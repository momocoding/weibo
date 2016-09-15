var log = function(){
    console.log(arguments)
}

var api = {}
api.ajax = function(url, method, form, callback){
    var request = {
        url: url,
        type: method,
        data: form,
        success: function(response){
            var r = JSON.parse(response)
            callback(r)
        },
        error: function(){
            var r = {
                success: false,
                message: '网络中断',
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.commentAdd = function(form, callback){
    var url = '/api/comment/add'
    var method = 'post'
    api.ajax(url, method, form, callback)
}
api.weiboAdd = function(form, callback){
    var url = '/api/weibo/add'
    var method = 'post'
    api.ajax(url, method, form, callback)
}
api.weiboDelete = function(url, callback){
    var method = 'get'
    var form = {}
    api.ajax(url, method, form, callback)
}
api.weiboUpdate = function(url, form, callback){
    var method = 'post'
    api.ajax(url, method, form, callback)
}