function Folder(elementForm, elementTree) {
    this.service = new Server();
    this.form = elementForm;
    this.tree = elementTree

};
Folder.prototype = {

    async deleteFolder(){
        const id = this.form.querySelector('*[name="id"]').value
        return this.service.deleteFolder(id).then( (data) => {
            const jsonReturn = JSON.parse(data);
            if (jsonReturn.deleted){
                this.tree.querySelector(`li[data-id="${id}"]`).remove()
            }
            const modal = bootstrap.Modal.getInstance(document.querySelector('#delete_folder'))
            modal.hide()
        });
    },
    async addSaveFolder(){
        id = this.form.querySelector('*[name="id"]').value
        nameFolder = this.form.querySelector('*[name="name"]').value
        parent_id = this.form.querySelector('*[name="id_parent_dir"]').value

        return this.service.addSaveFolder(id, nameFolder, parent_id).then( (data) => {
            
            const jsonReturn = JSON.parse(data);
            if (jsonReturn.created){
                const dropdown = document.createElement('li');
                dropdown.className = 'mb-1';
                dropdown.setAttribute('style',"margin-left:10px")
                dropdown.setAttribute('data-id', jsonReturn.id)
                dropdown.innerHTML  = `<div class="dropdown-context-menu" data-option="#context-menu-folder">
                                            <button class="btn btn-toggle align-items-center rounded " data-bs-toggle="collapse" data-bs-target="#folder-${jsonReturn.id}" aria-expanded="false">
                                                <i class="bi bi-caret-right"></i> 
                                            </button>
                                            <span role="button" class="selection-element folder" data-selection=".folder" data-id="${jsonReturn.id}">${nameFolder}</span>
                                        </div>
                                        <div class="collapse show" id="folder-${jsonReturn.id}">
                                            <ul class="list-unstyled btn-toggle-nav fw-normal pb-1">
                                            
                                            </ul>
                                        </div>`
                this.tree.querySelector(`li[data-id='${parent_id}'] ul`).appendChild(dropdown)
                document.querySelector('#id_parent_folder').innerHTML += `<option value="${jsonReturn.id}">${nameFolder}</option>`
                
            } else {
                const element = this.tree.querySelector(`li[data-id='${id}']`);
                element.querySelector(`span.folder[data-id='${id}']`).textContent = nameFolder;
                if (element.getAttribute('data-parent') != parent_id){
                    this.tree.querySelector(`li[data-id='${parent_id}'] ul`).appendChild(element)
                }
            }
            const modal = bootstrap.Modal.getInstance(document.querySelector('#add_edit_folder'))
            modal.hide()
        });
    },
}
/*
<li class="mb-1" style="margin-left:10px" data-id="9">
            <div class="dropdown-context-menu" data-option="#context-menu-folder">
                <button class="btn btn-toggle align-items-center rounded " data-bs-toggle="collapse" data-bs-target="#folder-9" aria-expanded="false">
                    <i class="bi bi-caret-right"></i> 
                </button>
                <span role="button" class="selection-element folder" data-selection=".folder" data-id="9">pasta 2.1.1</span>
            </div>
            <div class="collapse show" id="folder-9">
                <ul class="list-unstyled btn-toggle-nav fw-normal pb-1">
                
                </ul>
            </div>
        </li>
            */