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
        svTable() {
            this.saveTable()
        },
        // Показать поле редактирование и скрыть все остальные 
        edTable() {
            this.saveTable();
            this.vis = false;
        },
        saveTable() {
            app.tdArray[this.id].qtext = this.question;
            app.tdArray[this.id].atext = this.answer;
            this.vis = true;
        }

    },
    created() {

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
        activCat: 0,

        loadButtom: false,
        status: false,
        modal: false,
        timerId: null
    },
    methods: {
        //Работа со списком категорий
        noModal: function () {
            this.saveListCategotyOnServer;
            this.modal = true;
        },
        offModal: function () {
            this.saveListCategotyOnServer;
            this.modal = false;
        },
        deletCat: function (index) {
            axi.get('settings',{
                params: {
                    params: 'deleteCat',
                    name: app.listCategory[index].name,
                }
            })
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                });

            if (this.listCategory.length !== 1) {
                if (index === this.activCat) {
                    if (this.listCategory.length === index + 1) {
                        this.activCat = index - 1;
                        this.listCategory[index - 1].activ = true;
                        this.getTDformCat(index - 1);
                    } else {
                        this.activCat = index;
                        this.listCategory[index + 1].activ = true;
                        this.getTDformCat(index + 1);
                    }
                }
            } else {
                this.tdArray = [];
                this.activCat = 0;
            }
            this.listCategory.splice(index, 1);
        },
        addCat: function (index) {
            if (this.listCategory.length === 0) {
                active = true;
            } else {
                active = false;
            }
            this.listCategory.push({
                id: this.nextCat++,
                name: 'Новая категория ' + this.nextCat,
                activ: active,
            });
            axi.get('/settings',{
                params:{
                    params: 'newCat',
                    name: 'Новая категория ' + this.nextCat
                }    
            })
                .then(function(response){
                    console.log(response)
                })
                .catch(function (error) {
                    console.log(error)
                })
            
        },
        editCat: function (index, value) {
            //TODO Поиск одинаковых названий категорий
            clearTimeout(this.timerId);
            if (typeof this.listCategory[index].old === 'undefined'){
                this.listCategory[index].old = this.listCategory[index].name;
            }
            this.listCategory[index].name=value;
            this.timerId = setTimeout(function () {
                //console.log(app.listCategory[index]);
                axi.get('/settings',{
                    params: {
                        params: 'renameCategory',
                        newName: value,
                        name: app.listCategory[index].old
                    }
                })
                    .then(function (response) {
                        console.log(response);
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
               // console.log(app.listCategory[index]);
                app.listCategory[index].old=undefined;

            }, 2000);
        },
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
            axi.post('/set', {
                td: this.tdArray,
                name: app.listCategory[this.activCat].name + '.csv',
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

        //Загрузка данных с категории по индексу
        getTDformCat: function (index) {
            this.nextTodoId = 0;
            this.tdArray = [];
            axi.get('/get', {
                params: {
                    name: app.listCategory[index].name
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
        },
        //Выбор категории
        loadCat: function (index) {

            if (index == this.activCat) {
                return
            }
            this.listCategory[this.activCat].activ = false;
            this.listCategory[index].activ = true;
            this.activCat = index;

            this.getTDformCat(index);


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
                        name: element.slice(0, -4),
                        activ: first,
                    });
                    if (first) {
                        app.activCat = 0;
                    }
                    app.nextCat++;
                    first = false;

                })
            ))
            .catch(function (error) {
                console.log(error);
            });

    },
})
