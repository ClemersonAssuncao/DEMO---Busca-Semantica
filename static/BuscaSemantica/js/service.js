function Server() {
    
}

Server.prototype = {

    async addSaveFolder(id, name, parent_id) {
        const parameter = new FormData();
        parameter.append('id', id);
        parameter.append('name', name);
        parameter.append('id_parent_dir', parent_id);
        return await this.send('POST', `/documents/folder/${id}`, parameter);
    },
    async deleteFolder(id) {
        return await this.send('POST', `/documents/delete_folder/${id}`);
    },
    getCrtfToken() {
        return document.getElementsByName('csrfmiddlewaretoken')[0].value;
    },
    send(method, url, parameter){
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();  
            xhr.open(method, url);
            xhr.setRequestHeader('X-CSRFToken', this.getCrtfToken());  
            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    console.log(event)
                }
            };
            
            xhr.onload = function () {
                if (this.status >= 200 && this.status < 300) {
                    resolve(xhr.response);
                } else {
                    reject({
                        status: this.status,
                        statusText: xhr.statusText
                    });
                }
            };
            xhr.onerror = function () {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            };
            xhr.send(parameter || new FormData());
        });
    },
}