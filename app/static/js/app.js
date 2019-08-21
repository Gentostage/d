const axi = axios.create();
const Toast = Swal.mixin({
// success
// error
// warning
// info
// question
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 1000
});

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
            this.saveTable();
            this.saveTdLine();
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
        },
        saveTdLine: function () {
            axi.put('/data', {
                question: this.question,
                answer: this.answer,
                name: app.listCategory[app.activCat].name + '.csv',
                id: this.id
            })
                .then(function (response) {
                    console.log(response)
                    Toast.fire({
                        type: 'success',
                        title: 'Сохранено'
                    })
                })
                .catch(function (error) {
                    Toast.fire({
                        type: 'error',
                        title: 'Ошибка сохранения'
                    })
                    console.log(error)})
        },
        remTd: function () {
            app.tdArray.splice(this.id, 1)
            axi.delete('/data', {
               data:{
                   name: app.listCategory[app.activCat].name + '.csv',
                   id: this.id
               }
            })
            .then(function (response) {
                Toast.fire({
                    type: 'success',
                    title: 'Удаленно'
                })
                console.log(response)})
            .catch(function (error) {
                Toast.fire({
                    type: 'error',
                    title: 'Ошибка удаления'
                })
                console.log(error)})
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
            console.log(app.listCategory[index].name)
            axi.delete('/category',{
                data:{
                    name: app.listCategory[index].name,
                }
            })
                .then(function (response) {
                    console.log(response);
                    Toast.fire({
                        type: 'success',
                        title: 'Категория удалена'
                    })
                })
                .catch(function (error) {
                    console.log(error);
                    Toast.fire({
                        type: 'error',
                        title: 'Ошибка удаления'
                    })
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
                alert: false,
            });
            axi.post('/category',{
                name: 'Новая категория ' + this.nextCat
            })
                .then(function(response){
                    console.log(response)
                     Toast.fire({
                        type: 'success',
                        title: 'Категория создана'
                    })
                })
                .catch(function (error) {
                    console.log(error)
                    Toast.fire({
                        type: 'error',
                        title: 'Ошибка создания'
                    })
                })
            
        },
        editCat: function (index, value) {
            value=value.replace(/^\s*/,'').replace(/\s*$/,'');
            let v= this.compareCat(value,index);
            if(v){
                this.listCategory[index].alert='Имя "'+v+'" уже используеться';
                this.listCategory[index].name=value;
            }else if (this.listCategory[index].alert){
                this.listCategory[index].alert=false;
            }
            if (value.length>50){
                this.listCategory[index].alert='Имя не должно быть больше 50 символов';
                this.listCategory[index].name=value;
            }
            if (typeof this.listCategory[index].old === 'undefined'){
                this.listCategory[index].old = this.listCategory[index].name;
            }

            this.listCategory[index].name=value;
            clearTimeout(this.timerId);
            this.timerId = setTimeout(function () {
                if(!app.listCategory[index].alert)
                {
                    axi.put('/category', {
                            newName: value,
                            name: app.listCategory[index].old
                    })
                        .then(function (response) {
                            console.log(response);
                        })
                        .catch(function (error) {
                            console.log(error)
                             Toast.fire({
                                type: 'error',
                                title: 'Ошибка'
                            })
                        })
                    app.listCategory[index].old = undefined;
                }

            }, 2000);
        },
        // Добавялем новое обращение
        //todo Сделать сохранение новой строки в таблице на сервере
        addTD: function () {
            this.tdArray.push({
                id: this.nextTodoId++,
                qtext: this.qtext,
                atext: this.atext,
            });
            window.scrollTo(0, document.body.scrollHeight);
        },
        compareCat: function(v, i){
            let r = false;
            this.listCategory.forEach(function (value, index, array) {
                if(index!==i && value.name.toUpperCase()===v.toUpperCase()){
                    r= value.name;
                }
            });
            return r;
        },

        // Сохраняем все обращения
        svTD: function () {
            axi.post('/setOld', {
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
            axi.get('/settings/relern', {
                timeout: 1000000,
                params: {
                    key: 'ECA1B4346991DCB90A179D35AC49AC08',
                }

            })
                .then(function (response) {
                    console.log(response);
                    app.loadButtom = false;
                    Toast.fire({
                        type: 'success',
                        title: 'Модель обученна'
                    })
                })
                .catch(function (error) {
                    console.log(error);
                    Toast.fire({
                        type: 'error',
                        title: 'Что то пошло не так('
                    })
                });
        },

        //Загрузка данных с категории по индексу
        getTDformCat: function (index) {
            this.nextTodoId = 0;
            this.tdArray = [];
            axi.get('/data', {
                params: {
                    name: app.listCategory[index].name
                }
            })
                .then(function (response) {
                    console.log(response);
                    response.data.forEach(function (element) {
                        app.tdArray.push({
                            id: app.nextTodoId++,
                            qtext: element['Question'],
                            atext: element['Answer'],
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
    {//Получение списка вопросов и ответов при загрузке страницы`
        axi.get('/data', {
            params: {
                name: 'default'
            }
        })
            .then(response => (
                response.data.forEach(function (element) {
                    app.tdArray.push({
                        id: app.nextTodoId++,
                        qtext: element['Question'],
                        atext: element['Answer'],
                    });
                })
            ))
            .catch(function (error) {
                console.log(error);
            });

        first = true;
        axi.get('/data/list')
        .then(response => (
            response.data.forEach(function (element) {
                app.listCategory.push({
                    id: app.nextCat,
                    name: element.slice(0, -4),
                    activ: first,
                    alert: false,
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
