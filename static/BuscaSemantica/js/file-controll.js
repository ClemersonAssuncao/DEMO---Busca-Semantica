function FileForm(formElement) {
    this.$element = formElement;
    this.init();
};
FileForm.prototype = {

    init() {
        if (!this.$element)
            return;
        this.$element.addEventListener('submit', e => {
            e.preventDefault(); 
            this.save();
        });
        const deleteFile = this.$element.querySelector('#delete-file');
        if (deleteFile){
            this.deleteFile = deleteFile
            this.deleteFile.addEventListener('click', e => {

                const check = this.deleteFile.classList.contains('active');
                this.deleteFile.parentElement.classList.toggle('text-decoration-line-through', check);
            })
            // <input type="checkbox" name="file-clear" id="file-clear_id">
        }
    },

    save() { 
        const parameter = new FormData();
        const file = this.$element.querySelector('input[name="file"]').files[0];
        const id = this.$element.querySelector('input[name="id"]').value;
        const url = id ? `edit/${id}` : 'add/';
        parameter.append('id', id);
        parameter.append('name', this.$element.querySelector('input[name="name"]').value);
        parameter.append('description', this.$element.querySelector('textarea[name="description"]').value);
        parameter.append('file', file);
        parameter.append('id_folder', this.$element.querySelector('select[name="id_folder"]').value);
        if (this.deleteFile){
            parameter.append('delete_file', this.deleteFile.classList.contains('active'))
        }
        const server = new Server(`${ file ? 'bi-filetype-pdf' : 'bi-file-earmark-text'}`);
        server.send('POST', `/documents/${url}`, parameter).then( dataSerialized => {
            const data = JSON.parse(dataSerialized);

            if (data.saved){
                window.location.href = "/documents/";
            } else {
                if (data.error){
                    const modalElement = document.querySelector('#errors-message');
                    modalElement.querySelector('.modal-body').textContent = data.error;
                    const modal = new bootstrap.Modal(modalElement)
                    modal.show();
                }
            }
        })
    },

}