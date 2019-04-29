
const axi = axios.create();

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
        id: Number
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
        // Сохранить кнопка 
        svTable: function(index){
            app.tdArray[this.id].qtext=this.question
            app.tdArray[this.id].atext=this.answer
            this.vis = true
  
        },
        // Показать поле редактирование и скрыть все остальные 
        edTable() {
            app.$emit("invis", true);
            this.vis = false
        },

    },
    created(){
        // Сохранить ВСЕ изменениев таблице и закрыть текстовое поле
        app.$on("invis", (vis)=>{
            app.tdArray[this.id].qtext=this.question
            app.tdArray[this.id].atext=this.answer
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
        loadButtom: false,
        status: false,
    },
    methods: {
        // Добавялем новое обращение 
        addTD: function () {
            this.tdArray.push({
                id: this.nextTodoId++,
                qtext: this.qtext,
                atext: this.atext,
            })
        },
        // Сохраняем все обращения 
        svTD: function () {
            this.$emit("invis", true);

            axi.post('/set',{
                td: this.tdArray
            })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        // перезапустить и обучить нейросеть
        refrDp: function(){
            this.loadButtom = true
            axi.get('/settings',{
                timeout: 1000000,
                params: {
                    key: 'ECA1B4346991DCB90A179D35AC49AC08',
                    relenr: 'on'
                }
                
            })
            .then(function (response) {
                console.log(response);
                app.loadButtom = false;
            })
            .catch(function (error) {
                console.log(error);
            });
        },

    },
    created()
    // init()
    {
        //Получение списка вопросов и ответов
        axi
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
