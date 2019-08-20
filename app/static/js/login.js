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

var app = new Vue({
    delimiters: ['${', '}'],
    el: '#tab',
    data: {
        mes: 'Логин'
    }
});