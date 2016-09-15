var commentAddTemplate = function(comment){
    var c = comment
    var t = `
        <div class="weibo-sub-comment clear-fix">
            <div class="weibo-comment-counter left">
            </div>
            <div class="weibo-username left">
               ${ c.user_id}:
            </div>
            <div class="right">
                ${ c.created_time}
            </div>
            <div class="left comment-sub-content">
                ${c.content}
             </div>
        </div>
        `
    return t
}

var weiboAddTemplate = function(weibo){
    var w = weibo
    var t = `
        <div class="weibo-cell">
            <div class="weibo-sub-content shadow clear-fix">
                <div class="weibo-username left clear-fix">
                    <a href="#">${ w.user_id }</a>
                </div>
                <div class="weibo-sub-content-info clear-fix right">
                    <div class="left">
                        ${ w.created_time }
                    </div>
                    <div class="left">
                        <button data-id="${ w.id }" class="delete-button ">删除</button>
                    </div>
                    <div class="left">
                        <button data-id="${ w.id }" class="update-button ">更新</button>
                    </div>
                    <div class="left">
                        <button data-id="${ w.id }" class="comment-button ">评论</button>
                    </div>
                </div>
                <div class="clear-fix line"></div>
                <div class="left sub-content-left">
                    <span>
                        ${ w.content }
                    </span>
                </div>
                <div class="right comment-counter">

                </div>
            </div>
            <div class="hide weibo-update clear-fix" id="td-${ w.id }-update">
                <div class="left" id="update-td">
                    <input class="weibo-input-update" type="text" name="update" placeholder=" 更新...">
                </div>
                <div class="right">
                    <button data-id="${ w.id }" class="weibo-button-update ">修改微博</button>
                </div>
            </div>
            <div class="hide weibo-comment " id="td-${ w.id }-comment">
                <div class="weibo-comment-content">
                </div>
                <div class="sub-comment-new clear-fix">
                    <div class="left" id="comment-td">
                        <input type="hidden" class="add-comment-id" name="weibo_id" value=${ w.id }>
                        <input type="text" class="add-comment-content" name="content" placeholder=" 评论...">
                    </div>
                    <div class="right ">
                        <button class="button_comment">评论微博</button>
                    </div>
                </div>
            </div>
        </div>
        `
    return t
}

$(document).ready(function(){
    var log = function(){
        console.log(arguments)
    }

    $(".weibo-sub-main").on('click', '.comment-button',function(){
        var weiboId = $(this).data('id')
        var selector = '#td-' + weiboId + '-comment'
        var div = $(selector)
        div.slideToggle();
    })

    $('.weibo-sub-main').on('click', '.update-button', function(){
        var weiboId = $(this).data('id')
        var selector = '#td-' + weiboId + '-update'
        var div = $(selector)
        div.slideToggle();
    })

    $('.weibo-comment-content').each(function(){
        var comments = $(this).children().length
        var counterDiv = $(this).parent().prevAll('.weibo-sub-content').children('.comment-counter')
        counterDiv.append(comments)
    })

    // 添加评论 AJAX
    $('.weibo-sub-main').on('click','.button_comment', function(){
        var button = $(this)
        var parent = button.parent().parent()
        var weibo_id = parent.find('.add-comment-id').val()
        var content = parent.find('.add-comment-content').val()
        log(weibo_id,'weibo_id', content, 'content')
        var weibo = {
            'weibo_id': weibo_id,
            'content': content
        }
        var response = function(r){
            if(r.success == true) {
                var c = r.data
                var div = parent.parent().children('.weibo-comment-content')
                div.append(commentAddTemplate(c))
                alertify.success(r.message)
            }else if(r.success == 302) {
                window.location.href = '/'
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        }
        api.commentAdd(weibo, response)
    })

    // 添加微博 AJAX
    $('.weibo-button-commit').on('click', function(){
        var content = $('.weibo-textarea-add').val()
        var weibo = {
            'content': content
        }
        var response = function(r){
            if(r.success) {
                var w = r.data
                var div = $('.weibo-sub-main')
                div.prepend(weiboAddTemplate(w))
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        }
        api.weiboAdd(weibo, response)
    })

    // 删除微博 AJAX
    $('.weibo-sub-main').on('click','.delete-button', function(){
        var weibo_id = $(this).data('id')
        var div = $(this).closest('.weibo-cell')
        var url = '/api/weibo/delete/' + weibo_id
        var response = function(r){
            if(r.success) {
                div.slideUp()
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        }
        api.weiboDelete(url, response)
    })

    // 更新微博 AJAX
    $('.weibo-sub-main').on('click','.weibo-button-update', function(){
        var weibo_id = $(this).data('id')
        var content = $(this).parent().prevAll('#update-td').children('.weibo-input-update').val()
        log(content,'content')
        var weibo = {
            content: content,
        }
        var url = '/api/weibo/update/' + weibo_id

        var div = $(this).parent().parent().parent().children('.weibo-sub-content').children('.sub-content-left').children()

        var response = function(r){
            if(r.success) {
                var content = r.data.content
                // this 放在函数里面会出大问题，猜测每个函数都有它的this
                log('div', div.attr("class"))
                log('content', content)
                div.html(content)
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        }
        api.weiboUpdate(url, weibo, response)
    })
})
