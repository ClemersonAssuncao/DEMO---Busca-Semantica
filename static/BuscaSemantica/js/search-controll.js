function Search( elementInput, elementList) {
    this.$elementInput = elementInput;
    this.$elementList = elementList;
    this.modalView = document.querySelector('#view_search');
    this.init();
};
Search.prototype = {

    init(){
        this.$elementInput.addEventListener('keyup', event => {
            var key= event.keyCode || event.which;
            if (key==13){
                this.search();
            }
        })
    },

    search(){
        const text = this.$elementInput.value;

        this.$elementList.innerHTML = '' ;

        const formData = new FormData();

        formData.append('text',text);

        const server = new Server('bi-search');
        server.send('POST', '/', formData).then( dataSerialized => {
            const data = JSON.parse(dataSerialized);
            console.log(data);
            if(data.error){
                const modalElement = document.querySelector('#errors-message');
                modalElement.querySelector('.modal-body').textContent = data.error;
                const modal = new bootstrap.Modal(modalElement)
                modal.show();
                return
            }

            for (const result of data.items) {

                const card = document.createElement('div');
                card.className = 'card border d-flex flex-column mb-2';
                card.setAttribute('role','button');

                card.innerHTML = `  <div class="row g-0">
                                        <div class="col-md-10">
                                            <div class="card-body">
                                                <h5 class="card-title">
                                                    <i class="bi ${result.file? 'bi-filetype-pdf': 'bi-card-text'} text-primary"></i>
                                                    <span>${result.name}</span>
                                                </h5>
                                                <p class="card-text">...${result.text}...</p>
                                                <p class="card-text">
                                                    <small class="text-body-secondary">
                                                        <i class="bi bi-pencil-fill text-secondary px-2"></i>
                                                        <span>Criado por ${result.user_created} em ${result.dt_created} </span>
                                                    </small>
                                                </p>
                                            </div>
                                        </div>
                                    </div>`;
                card.addEventListener('click', () => {
                    if (!this.modalView['instance'])
                        this.modalView['instance'] = new bootstrap.Modal(this.modalView, {});

                        // subsituir os dados do HTML com o item selecionado;
                        this.modalView.querySelector('.modal-title').textContent = result.name;

                        // incluir outros campos
                        this.modalView.querySelector('.modal-description').textContent = result.description;

                        this.modalView.querySelector('#button-view').setAttribute('href', ´/documents/edit/${result.id}´);

                        this.modalView['instance'].show();
                })
                this.$elementList.appendChild(card);
            }
        })
    }
}
