function Folder(elementForm, elementTree) {
    this.service = new Server();
    this.form = elementForm;
    this.tree = elementTree

};
Folder.prototype = {

    async addSaveFolder(){
        id = this.form.querySelector('*[name="id"]').value
        nameFolder = this.form.querySelector('*[name="name"]').value
        parent_id = this.form.querySelector('*[name="id_parent_dir"]').value

        this.service.addSaveFolder(id, nameFolder, parent_id).then( (botText) => {
            console.log(botText)
        });
    },
}