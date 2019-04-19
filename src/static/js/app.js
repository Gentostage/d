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
        svTable(){
            app.tdArray[this._uid-1].qtext=this.question
            app.tdArray[this._uid-1].atext=this.answer
            
            this.vis = true
  
        },
        edTable() {
            app.$emit("invis", true);
            this.vis = false
        },
    },
    created(){
        app.$on("invis", (vis)=>{
            app.tdArray[this._uid-1].qtext=this.question
            app.tdArray[this._uid-1].atext=this.answer
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
        },
    },
    created()
    {
        axios
            .get('http://localhost:3030/get')
            .then(response => (
                response.data.forEach(function(element) {
                if (element[0] == 'Question'){
                }else
                {
                app.tdArray.push({
                    id: app.nextTodoId++,
                    qtext: element[0],
                    atext: element[1],
                })
                }
            })
            ));
    },
})
