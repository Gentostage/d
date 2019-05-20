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
        svTable () {
            this.saveTable()
        },
        // Показать поле редактирование и скрыть все остальные 
        edTable() {
            app.$emit("invis");
            this.vis = false
        },
        saveTable(){
            app.tdArray[this.id].qtext = this.question;
            app.tdArray[this.id].atext = this.answer;
            this.vis = true;
        }

    },
    created() {
        // Сохранить ВСЕ изменениев таблице и закрыть текстовое поле
        app.$on("invis", ()=>  {
            this.saveTable()
        });
    },

});

var app = new Vue({
    delimiters: ['${', '}'],
    el: '#tab',
    data: {
        tdArray: [],
        nextTodoId: 0,
        qtext: 'Вопрос',
        atext: 'Ответ',

        listCategory: [],
        nextCat: 0,
        activCat: [],

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
            });
            window.scrollTo(0, document.body.scrollHeight);
        },
        // Сохраняем все обращения 
        svTD: function () {
            this.$emit("invis", true);

            axi.post('/set', {
                td: this.tdArray,
                name: app.activCat.text+'.csv',
            })
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        // перезапустить и обучить нейросеть
        refrDp: function () {
            this.loadButtom = true;
            axi.get('/settings', {
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
        //Загрузка категории
        loadCat: function (loadCat, index) {

            if (index == this.activCat.id){
                return
            }
            this.listCategory[this.activCat.id].activ=false;
            this.listCategory[index].activ=true;
            this.activCat=this.listCategory[index];

            this.nextTodoId = 0;
            this.tdArray = [];
            axi.get('/get', {
                params: {
                    name: loadCat
                }
            })
            .then(function (response) {
                console.log(response);
                response.data.forEach(function (element) {
                    app.tdArray.push({
                        id: app.nextTodoId++,
                        qtext: element[0],
                        atext: element[1],
                    })
                })
                })
                .catch(function (error) {
                    console.log(error);
                });

        }
    },
    beforeCreate()
    // init()
    {//Получение списка вопросов и ответов при загрузке страницы
        axi.get('/get', {
            params: {
                name: 'default'
            }
        })
            .then(response => (
                response.data.forEach(function (element) {
                    app.tdArray.push({
                        id: app.nextTodoId++,
                        qtext: element[0],
                        atext: element[1],
                    });
                })
            ))
            .catch(function (error) {
                console.log(error);
            });

        first = true;
        axi.get('/get', {
            params: {
                list: 'list'
            }
        })
        .then(response => (
            response.data.forEach(function (element) {
                app.listCategory.push({
                    id: app.nextCat,
                    text: element.slice(0, -4),
                    activ: first,
                });
                if(first){
                    app.activCat=app.listCategory[0];
                }
                app.nextCat++;
                first=false;

            })
        ))
        .catch(function (error) {
            console.log(error);
        });

    },
})
