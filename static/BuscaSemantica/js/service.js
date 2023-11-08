function Server(icon) {
    this.loader = document.querySelector('#loader-service');
    this.loader.querySelector('i').className = `bi ml-1 ${icon}`
}

Server.prototype = {
    
    getCrtfToken() {
        return document.getElementsByName('csrfmiddlewaretoken')[0].value;
    },
    send(method, url, parameter){
        this.loader.classList.remove('d-none');
        document.body.appendChild(this.loader);
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();  
            xhr.open(method, url);
            xhr.setRequestHeader('X-CSRFToken', this.getCrtfToken());  
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    // console.log(event)
                }
            };
            self = this;
            xhr.onload = function () {
                if (this.status >= 200 && this.status < 300) {
                    self.loader.classList.add('d-none')
                    resolve(xhr.response);
                } else {
                    self.loader.classList.add('d-none')
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