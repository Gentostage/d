Vue.component('tdinput', {
    delimiters: ['${', '}'],
    props: {
        qtext: {
            type: String,
            default: '',
            required: true
        },
        atext: {
            type: String,
            default: '',
            required: true
        },
    },
    data: function () {
        return {
            vis: true,
            question: this.qtext,
            answer: this.atext,

        }
    },
    template: '#tdinput ',
    methods: {
        svTable: function(index){
            app.tdArray.indexOf(this).qtext=this.question
            app.tdArray.indexOf(this).atext=this.answer
            this.vis = true
  
        },
        edTable() {
            app.$emit("invis", true);
            this.vis = false
        },

    },
    created(){
        app.$on("invis", (vis)=>{
            app.tdArray.indexOf(this).qtext=this.question
            app.tdArray.indexOf(this).atext=this.answer
            this.vis = vis;
            

        });
    },
 
})


var app = new Vue({
    delimiters: ['${', '}'],
    el: '#tab',
    data: {
        tdArray: [],
        nextTodoId: 0,
        qtext: 'Вопрос',
        atext: 'Ответ',
    },
    methods: {
        addTD: function () {
            this.tdArray.push({
                id: this.nextTodoId++,
                qtext: this.qtext,
                atext: this.atext,
            })
        },
        svTD: function () {
            console.log('svTD')
            this.$emit("invis", true);

            axios.post('/set',{
                td: this.tdArray
            })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        

    },
    created()
    {
        axios
            .get('/get')
            .then(response => (
                response.data.forEach(function(element) {
                app.tdArray.push({
                    id: app.nextTodoId++,
                    qtext: element[0],
                    atext: element[1],
                })
            })
            )) 
            .catch(function (error) {
                console.log(error);
            });;
    },
})
