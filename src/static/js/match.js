const axi = axios.create();

function Set(name, data){
    console.log(name,data)
    axi.put('/set/skills',{
        data:{
            name: name,
            data: data,
        }
    })
        .then(response=>{
            console.log(response)
        })
        .catch(error=>{
            console.log(error)
        })
}
function Get(){
    return axi.get('/get/skills',{
    })
        .then(response =>{
            console.log(response);
            return response.data;
        })
        .catch(response =>{console.log(response)});
}
function deleteId(array) {
    newArray = []
    array.forEach(function(data){
        newArray.push({
            name: data["value"]
        })
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
    methods:{
        add(name){
            if (name==='HelloResponse'){
                this.HelloResponse.push({
                    id: this.idHelloResponse++,
                    value: ''
                })
            }else if(name === 'HelloPattern'){
                 this.HelloPattern.push({
                    id: this.idHelloPattern++,
                    value: ''
                })
            }
            console.log(name)
        },
        save(name){
            if(name ==='Hello'){
                Pattern =deleteId(this.HelloPattern)
                Response = deleteId(this.HelloResponse)
                data={
                    patterns: Pattern,
                    responses: Response,
                }
                Set(name, data)
            }

        }
    },
    created() {
        Get().then(data=>{
            helloResponses=data['hello']['responses'];
            Object.values(helloResponses).forEach(function (data) {
                mat.HelloResponse.push({
                    id: this.idHelloResponse++,
                    value: data
                })
            })
            helloPatterns=data['hello']['patterns'];
            Object.values(helloPatterns).forEach(function (data) {
                mat.HelloPattern.push({
                    id: this.idHelloPattern++,
                    value: data
                })
            })
            byeResponses=data['bye']['responses'];
            Object.values(byeResponses).forEach(function (data) {
                mat.ByeResponse.push({
                    id: this.idByeResponse++,
                    value: data
                })
            })
            byePatterns=data['bye']['patterns'];
            Object.values(byePatterns).forEach(function (data) {
                mat.ByePattern.push({
                    id: this.idByePattern++,
                    value: data
                })
            })
            fallbackResponses=data['fallback']['responses'];
            Object.values(fallbackResponses).forEach(function (data) {
                mat.FallbackResponses.push({
                    id: this.idFallback++,
                    value: data,
                })
            });
        });


    },
})