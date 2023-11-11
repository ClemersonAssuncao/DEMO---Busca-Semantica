function FolderTree( elementTree, filterElement) {
    this.$element = elementTree;
    this.$filterElement = filterElement;
    this.folders = [];
    this.events = {
        CREATED_FOLDER: 'created_folder',
        SPAN_CLICKED: 'span_clicked',
        DELETED_FOLDER: 'deleted_folder'
    }
    this.init();
};
FolderTree.prototype = {

    addEventListener(eventName, action){
        this.$element.addEventListener(eventName, action);
    },

    dispatchCardEvent(eventName, data = {}) {
        this.$element.dispatchEvent( new CustomEvent(eventName, {
            detail: data,
            cancelable: true,
          })
        );
    },

    delete() {
        this.currentElement;
        const formData = new FormData();
        formData.append('id', this.currentElement.id);
        const server = new Server('bi-folder-x');
        server.send('POST', `/documents/delete_folder/${this.currentElement.id}`, formData).then( dataSerialized => {
            const data = JSON.parse(dataSerialized);
            if (data.deleted){
                this.folders = this.folders.filter( folder => folder.id != this.currentElement.id );
                const removeChild = ( item ) => {
                    const elements = item.parentElement.querySelectorAll(`div[data-parent="${item.getAttribute('data-id')}"]`);
                    for (const element of elements) {
                        const id = element.getAttribute('data-id');
                        document.querySelector(`#id_parent_folder option[value="${id}"]`).remove();
                        this.dispatchCardEvent(this.events.DELETED_FOLDER, {'id': id})
                        removeChild(element);
                    }
                }
                removeChild(this.currentElement.$element);
                document.querySelector(`#id_parent_folder option[value="${this.currentElement.id}"]`).remove();
                this.dispatchCardEvent(this.events.DELETED_FOLDER, {'id': this.currentElement.id})
                this.currentElement.$element.parentElement.remove();
                this.modalDelete['instance'].hide();
            } else {
                this.modalDelete.querySelector('.text').textContent = 'Não foi possível excluir por existir documentos vinculados a essa pasta ou a uma pasta filho:';
                this.modalDelete.querySelector('.error').innerHTML = '';
                this.modalDelete.querySelector('#button-delete').classList.add('d-none')
                for (const file of data.error) {
                    const link = document.createElement('a');
                    link.className = 'text-danger nav-link';
                    link.textContent = `${file.id} - ${file.name} `;
                    link.setAttribute('href', `/documents/edit/${file.id}`);
                    this.modalDelete.querySelector('.error').appendChild(link);
                }
            }
        });
    },

    save(){
        this.currentElement.id = this.modalAddEdit['formElement'].querySelector('input[name="id"]').value;
        this.currentElement.name = this.modalAddEdit['formElement'].querySelector('input[name="name"]').value;
        this.currentElement.parent_id = this.modalAddEdit['formElement'].querySelector('select[name="id_parent_dir"]').value ;

        const formData = new FormData();
        formData.append('id', this.currentElement.id);
        formData.append('name', this.currentElement.name);
        if (this.currentElement.parent_id !== '')
            formData.append('id_parent_dir', this.currentElement.parent_id );

        const server = new Server('bi-folder-fill');
        server.send('POST', `/documents/folder/${this.currentElement.id}`, formData).then( dataSerialized => {
            const data = JSON.parse(dataSerialized);

            if (data.created){
                const li = document.createElement('li');
                li.className = 'mb-1';
                li.setAttribute('style', 'margin-left:10px');
                this.currentElement.setId(data.id);
                this.currentElement.setName(data.name);
                this.currentElement.setParent(data.id_parent_dir);
                const newElement = this.currentElement.createElement();
                li.appendChild(newElement);
                
                const collapseItem = document.createElement('div');
                collapseItem.className = 'collapse show';
                collapseItem.setAttribute('id',`folder-${data.id}`)
                collapseItem.innerHTML = `<ul class="list-unstyled btn-toggle-nav fw-normal pb-1"> </ul>`;
                li.appendChild(collapseItem);
                this.addEventTreeItem(newElement, this.currentElement);
                if (data.id_parent_dir){
                    this.$element.querySelector(`.tree-item[data-id='${data.id_parent_dir}']`).nextElementSibling.querySelector('ul').appendChild(li);
                } else {
                    this.$element.appendChild(li);
                }
                new bootstrap.Collapse(collapseItem, { toggle: false })
                document.querySelector('#id_parent_folder').innerHTML += `<option value="${data.id}">${data.name}</option>`  
                this.folders.push(this.currentElement);
                this.dispatchCardEvent(this.events.CREATED_FOLDER, data)
            } else {
                this.currentElement.$element.setAttribute('data-name', data.name);
                this.$element.querySelector(`.tree-item[data-id='${data.id}'] span`).textContent = data.name;
                
                if (this.currentElement.$element.getAttribute('data-parent') != (data.id_parent_dir || '')){
                    this.currentElement.$element.setAttribute('data-parent', data.id_parent_dir);
                    if (!data.id_parent_dir){
                        this.$element.appendChild(this.currentElement.$element);
                    } else {
                        this.$element.querySelector(`.tree-item[data-id='${data.id_parent_dir}']`).nextElementSibling.querySelector('ul').appendChild(this.currentElement.$element);
                    }
                }
                document.querySelector(`#id_parent_folder option[value="${data.id}"]`).textContent = data.name;
            }
            this.modalAddEdit['instance'].hide();
        });
        
    },

    viewModalDelete() {
        this.modalDelete.querySelector('.text').textContent = 'Deseja realmente excluir esta pasta?';
        this.modalDelete.querySelector('.error').innerHTML = '';
        this.modalDelete.querySelector('#button-delete').classList.remove('d-none')
        // Carregar informação no modal
        document.body.appendChild(this.modalDelete);
        if (!this.modalDelete['instance'])
            this.modalDelete['instance'] = new bootstrap.Modal(this.modalDelete, {});
        this.modalDelete['instance'].show();
    },

    viewModalAddEdit(folderInstance) {
        // Carregar informação no modal
        this.currentElement = folderInstance || this.currentElement;
        this.modalAddEdit.querySelector('#folder-action-title').textContent = (!this.currentElement.id)? 'Adicionar Pasta':'Editar Pasta';
        this.modalAddEdit['formElement'].querySelector('input[name="id"]').value = this.currentElement.id;
        this.modalAddEdit['formElement'].querySelector('input[name="name"]').value = this.currentElement.name;
        this.modalAddEdit['formElement'].querySelector('select[name="id_parent_dir"]').value = this.currentElement.parent_id || '';

        // Abrir modal
        document.body.appendChild(this.modalAddEdit);
        if (!this.modalAddEdit['instance'])
            this.modalAddEdit['instance'] = new bootstrap.Modal(this.modalAddEdit, {});
        this.modalAddEdit['instance'].show();
    },

    openContextMenu(event) {
        this.contextMenu.classList.add('show');
        if (document.body.clientHeight < this.contextMenu.clientHeight + event.screenY ){
            this.contextMenu.style.top = event.clientY - (this.contextMenu.clientHeight) +'px';
        } else {
            this.contextMenu.style.top = event.clientY - 5 + 'px';
        }
        this.contextMenu.style.left = event.clientX - 5 + 'px';
        document.body.appendChild(this.contextMenu);
    },

    init() {
        if (!this.$element){
            return;
        }

        // prepare context menu event's
        this.contextMenu = document.querySelector('#context-menu-folder');
        this.contextMenu.addEventListener('mouseleave', (e) => {
            e.fromElement.classList.remove('show');
        })
        this.$element.querySelectorAll('.tree-item').forEach( element => {
            const folder = new Folder(element)
            this.folders.push(folder);
            this.addEventTreeItem(element, folder);
        });

        // prepare modal and form
        this.modalAddEdit = document.querySelector('#add_edit_folder');
        this.modalDelete = document.querySelector('#delete_folder');
        this.modalAddEdit['formElement'] = this.modalAddEdit.querySelector('form');
        this.modalAddEdit['formElement'].addEventListener('submit', e => {e.preventDefault(); this.save();});

        //prepare Filter
        if (this.$filterElement){
            this.$filterElement.addEventListener('keyup', () => {
                const value = this.$filterElement.value;
                this.filter(value)
            })
        }
        const documentFilter = document.querySelector('#doc-name');
        if (documentFilter){
            documentFilter.addEventListener('keyup', () => {
                this.filterDocuments()
            })
        }

        
    },

    filter(text){
        // Esconde todos os itens da arvore
        this.$element.querySelectorAll('li').forEach(element => element.classList.add('d-none'))    

        for (const folder of this.folders) {                    

            const checked = folder.name.toUpperCase().includes(text.toUpperCase());
            if (checked){

                // apresenta o próprio elemento
                folder.$element.parentElement.classList.remove('d-none');

                // apresenta todos os filhos
                folder.$element.parentElement.querySelectorAll('li').forEach( element => {
                    element.classList.remove('d-none');
                });

                // Apresenta todos os pais
                const showParent = parent => {
                    if (parent.tagName == 'LI'){
                        parent.classList.remove('d-none');
                    }
                    if (parent.parentElement != this.$element)
                        showParent(parent.parentElement);
                }
                showParent(folder.$element.parentElement);
            } 
        }
    },

    addEventTreeItem(element, folder){
        element.addEventListener('contextmenu', (event) => {
            event.preventDefault();
            this.currentElement = folder;
            this.openContextMenu(event);
        });
        const span = element.querySelector('span');
        span.addEventListener('click', (event) => {
            
            if (span.classList.contains('selected')){
                this.filteredFolder = null;
                this.filteredSpan = null;
                span.classList.remove('selected')
            } else {
                if (this.filteredSpan){
                    this.filteredSpan.classList.remove('selected')
                }
                this.filteredFolder = element.getAttribute('data-id');
                this.filteredSpan = span;
                span.classList.add('selected');
            }
            this.dispatchCardEvent(this.events.SPAN_CLICKED, {'id': this.filteredFolder, 'span': span});
        });
    },
    filterDocuments() {
        const text = document.querySelector('#doc-name').value.toUpperCase();
        const id = this.filteredFolder;
        document.querySelectorAll(`table tbody tr td.id_folder`).forEach(el => {
            const checkedId = el.parentElement.querySelector('.id span').textContent.toUpperCase().includes(text);
            const checkedName = el.parentElement.querySelector('.name').textContent.toUpperCase().includes(text);
            const checkedDescription = el.parentElement.querySelector('.description').textContent.toUpperCase().includes(text);
            // const 
            // if ()
            // essa condição está errada
            // está filtrando por texto, porém não filtra por pasta
            // essa condição verifica pasta: id != null && el.getAttribute('data-id') != id
            // essa condição verifica o texto: !checkedId && !checkedName && !checkedDescription
            const checked = (id != null && el.getAttribute('data-id') != id) || (!checkedId && !checkedName && !checkedDescription);
            
            // O filtro deve funcionar tanto com pasta, quando texto, se utilizar o texto, deve considerar apenas os itens que estão
            // filtrados na pasta também, caso utilizado ambos os filtros;
            // Quando a condição abaixo recebe true, ele oculta a linha, do contrário ele mostra
            el.parentElement.classList.toggle('d-none', checked );
        })
    }
};

function Folder(folderElement) {
    this.$element = folderElement;
    this.id = null;
    this.name = null;
    this.parent_id = null;
    this.init();
};
Folder.prototype = {

    setId(id){
        this.id = id;
    },
    setName(name){
        this.name = name;
    },
    setParent(parent_id){
        this.parent_id = parent_id;
    },
    init(){
        if (this.$element){
            this.id = this.$element.getAttribute('data-id');
            this.name = this.$element.getAttribute('data-name');
            this.parent_id = this.$element.getAttribute('data-parent');
        }
    },
    createElement() {

        const treeItem = document.createElement('div');
        treeItem.className = 'dropdown-context-menu tree-item d-flex flex-row align-items-center';
        treeItem.setAttribute('data-id', this.id);
        treeItem.setAttribute('data-name', this.name);
        treeItem.setAttribute('data-parent', this.parent_id);
        treeItem.innerHTML = `<button class="btn btn-toggle align-items-center rounded " data-bs-toggle="collapse" data-bs-target="#folder-${this.id}" aria-expanded="false">
                                    <i class="bi bi-caret-right"></i> 
                                </button>
                                <span role="button" class='selection-element  d-flex w-100'>${this.name}</span>`;
        

        
        this.$element = treeItem;
        return this.$element;
   }

}