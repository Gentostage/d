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

function Set(name, data) {
    axi.put('/skills', {
        data: {
            name: name,
            data: data,
        }
    })
        .then(response => {
            Toast.fire({
                type: 'success',
                title: 'Сохранено'
            });
            console.log(response)
        })
        .catch(error => {
            Toast.fire({
                type: 'error',
                title: 'Ошибка сохранения'
            })
            console.log(error)
        })
}

function Align(Response, Pattern) {
    while (Response.length !== Pattern.length) {
        if (Response.length < Pattern.length) {
            Response.push(' ')
        } else if (Response.length > Pattern.length) {
            Pattern.push(' ')
        }
    }
    return {
        Response: Response,
        Pattern: Pattern
    }
}

function Get() {
    return axi.get('/skills', {})
        .then(response => {
            console.log(response);
            return response.data;
        })
        .catch(response => {
            console.log(response)
        });
}

function deleteId(array) {
    newArray = []
    array.forEach(function (data) {
        if (data['value']!=null){
            newArray.push(data["value"].replace(/^\s*/,'').replace(/\s*$/,''))
        }else if (data['value']===' '){
            newArray.push(null)
        }

    });
    return newArray
}

var mat = new Vue({
    delimiters: ['${', '}'],
    el: '#mat',
    data: {
        HelloPattern: [],
        idHelloPattern: 0,

        HelloResponse: [],
        idHelloResponse: 0,

        ByeResponse: [],
        idByeResponse: 0,

        ByePattern: [],
        idByePattern: 0,

        FallbackResponses: [],
        idFallback: 0,

    },
    methods: {
        add(name) {
            if (name === 'HelloResponse') {
                this.HelloResponse.push({
                    id: this.idHelloResponse++,
                    value: ''
                })
            } else if (name === 'HelloPattern') {
                this.HelloPattern.push({
                    id: this.idHelloPattern++,
                    value: ''
                })
            } else if (name === 'ByeResponse') {
                this.ByeResponse.push({
                    id: this.idByeResponse++,
                    value: ''
                })
            } else if (name === 'ByePattern') {
                this.ByePattern.push({
                    id: this.idByePattern++,
                    value: ''
                })
            } else if (name === 'FallbackResponses') {
                this.FallbackResponses.push({
                    id: this.idFallback++,
                    value: ''
                })
            }
        },
        save(name) {
            let Pattern;
            let Response;
            if (name === 'hello_skill') {
                Pattern = deleteId(this.HelloPattern);
                Response = deleteId(this.HelloResponse);
            } else if (name === 'bye_skill') {
                Pattern = deleteId(this.ByePattern);
                Response = deleteId(this.ByeResponse);
            } else if (name === 'fallback_skill') {
                Response = deleteId(this.FallbackResponses);
                let data = {
                    responses: Response,
                }
                Set(name, data);
                return 1
            }
            let tmp = Align(Response, Pattern);
            Pattern = tmp.Pattern;
            Response = tmp.Response;
            let data = {
                responses: Response,
                patterns: Pattern,
            };
            Set(name, data)
        }
    },
    created() {
        Get().then(data => {
            let helloResponses = data['hello']['responses'];
            Object.values(helloResponses).forEach(function (data) {
                if (data != null) {
                    mat.HelloResponse.push({
                        id: this.idHelloResponse++,
                        value: data
                    })
                }
            });
            let helloPatterns = data['hello']['patterns'];
            Object.values(helloPatterns).forEach(function (data) {
                if (data != null) {
                    mat.HelloPattern.push({
                        id: this.idHelloPattern++,
                        value: data
                    })
                }
            });
            let byeResponses = data['bye']['responses'];
            Object.values(byeResponses).forEach(function (data) {
                if (data != null) {
                    mat.ByeResponse.push({
                        id: this.idByeResponse++,
                        value: data
                    })
                }
            });
            let byePatterns = data['bye']['patterns'];
            Object.values(byePatterns).forEach(function (data) {
                if (data != null) {
                }
                mat.ByePattern.push({
                    id: this.idByePattern++,
                    value: data
                })
            });
            let fallbackResponses = data['fallback']['responses'];
            Object.values(fallbackResponses).forEach(function (data) {
                if (data != null) {
                mat.FallbackResponses.push({
                    id: this.idFallback++,
                    value: data,
                })
            }
        });
    })
;


},
})