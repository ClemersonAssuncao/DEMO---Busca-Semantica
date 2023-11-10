function Search( elementInput, elementList) {
    this.$elementInput = elementInput;
    this.$elementList = elementList;
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

        this.$elementList.innerHtml = '';

        const formData = new FormData();

        formData.append('text',text);

        const server = new Server('bi-search');
        server.send('POST', '/', formData).then( dataSerialized => {
            const data = JSON.parse(dataSerialized);
            console.log(data)
        })
    }
}