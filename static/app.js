const App = {
    data() {
        return {
            books: []
        }
    },
    mounted() {
        axios.get('api/books/')
        .then((response) => {
            this.books = response.data;
        })
    }
};

Vue.createApp(App).mount('#books_app')