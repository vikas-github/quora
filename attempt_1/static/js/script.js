$( document ).ready(function() {
    console.log( "ready!" );
    $('.share-answer-item').on('click', function(e){
        e.preventDefault();
        $('.modal.share_answer').modal('show');
        return false;
    });

    $('.upvote-answer-action, .downvote-answer-action').on('click', function(e){
        e.preventDefault();
        $button = $(this);
        $button_parent = $button.parents('.answer_item');
        $bp_uc = $button_parent.find('.upvote-answer-action');
        $bp_dc = $button_parent.find('.downvote-answer-action');

        $answer_id = $(this).attr('data-answer-id');
        $question_id = $(this).attr('data-question-id');
        $action_req = $(this).attr('data-vote');
        a_url =  '/'+$question_id+'/answer/'+$answer_id+'/vote/'+$action_req
        $.get(a_url, function(data, status) {
//            alert("Data: " + data + "\nStatus: " + status);
            console.log(status+" "+data);
            var obj = JSON.parse(data);
            if(obj.success == 'true'){
                if(obj.action == 'upvoted'){
                    $button.addClass('pressed');
                    $button_parent.find('.downvote-answer-action').removeClass('pressed');
                }else if(obj.action == 'downvoted'){
                    $button.addClass('pressed');
                    $button_parent.find('.upvote-answer-action').removeClass('pressed');
                }else if(obj.action == 'unvoted'){
                    $button_parent.find('.upvote-answer-action').removeClass('pressed');
                    $button_parent.find('.downvote-answer-action').removeClass('pressed');
                }
                var el = $('.vote-count')
                $bp_uc.find(el).text(obj.uc);
                $bp_dc.find(el).text(obj.dc);


            }else{
                var el = $('.vote-count')
                $bp_uc.find(el).text(obj.uc);
                $bp_dc.find(el).text(obj.dc);
                var item = $('<span class="badge badge-warning">'+obj.error+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));
            }

        }).fail(function() {
            var item = $('<span class="badge badge-warning">Could not reach server or bad link!</span>').hide();
            $('.sticky-badge').append(item);
            item.fadeIn(500, runEffect(item));
        });

        return false;
    });

    function runEffect($el) {
            setTimeout(function(){
            var selectedEffect = 'blind';
            var options = {};
            $el.fadeOut(100)
        }, 5000);
    }

    $('.ask_question_button').on('click', function(e){
        e.preventDefault();
        $('.modal.ask_question_modal').modal('show');
        return false;
    });

    $('.add_question_submit').on('click', function(e){
        e.preventDefault();
        q_text = $('.ask_question_modal .question_text_area textarea[name="question_text"]').val();
        csrf_token = $('.ask_question_modal .question_text_area input[name="csrfmiddlewaretoken"]').val();
        a_url =  '/add_question';

        data = {'question_text': q_text, csrfmiddlewaretoken: csrf_token};
        $.post(a_url, data, function(response, status) {
            console.log(status);
            var obj = JSON.parse(response);
            if(obj.success == 'true'){
                  $('.modal.ask_question_modal.show').modal("hide");
                  redirect_url = '/'+obj.qid;
                  window.location.href = '/'+redirect_url;

            }else{
                error_text = obj.error;
                $('.modal.ask_question_modal.show .add_question_error').find('.error_text').empty().append(error_text);
                $('.modal.ask_question_modal.show .add_question_error').removeClass('hide');
            }

        });
        return false;
    });

    $('.edit_question_text').on('click', function(e){
        e.preventDefault();
        qtxt = $(this).attr('data-question-text');
        qid = $(this).attr('data-qid');

        $('.edit_question_modal').find('textarea').val(qtxt);
        $('.edit_question_modal').find('input[name="qid"]').val(qid);
        $('.edit_question_modal').modal('show');

        return false;
    });

    $('.change_question_text_submit').on('click', function(e){
        e.preventDefault();

        q_text = $('.edit_question_modal .question_text_area textarea[name="question_text"]').val();
        qid = $('.edit_question_modal .question_text_area input[name="qid"]').val();
        csrf_token = $('.edit_question_modal .question_text_area input[name="csrfmiddlewaretoken"]').val();
        a_url =  '/edit_question';

        data = {'question_text': q_text, 'question_id': qid, csrfmiddlewaretoken: csrf_token};
        $.post(a_url, data, function(response, status) {
            console.log(status);
            var obj = JSON.parse(response);
            if(obj.success == 'true'){
                  $('.modal.edit_question_modal.show').modal("hide");
                  elem_s = '.uni_question_id_'+qid;
                  elem_h = '.edit_question_text[data-qid="'+qid+'"]';
                  $(elem_s).empty().append(q_text);
                  $(elem_h).attr('data-question-text',q_text);


            }else{
                error_text = obj.error;
                $('.modal.edit_question_modal.show .add_question_error').find('.error_text').empty().append(error_text);
                $('.modal.edit_question_modal.show .add_question_error').removeClass('hide');
            }

        });


        return false;
    });

    $('.user_comment_submit').on('click', function(e){
        e.preventDefault();
        button = $(this);
        parent_list = button.parents('.comments_block');
        ctext = $(this).siblings('.user_comment_input').val();
        aid = $(this).attr('data-answer');
        qid = $(this).attr('data-question');
        csrf_token = $(this).siblings('input[name="csrfmiddlewaretoken"]').val();
        a_url =  '/'+qid+'/answer/'+aid+'/comment';
        data = {'ctext': ctext, 'aid': aid, csrfmiddlewaretoken: csrf_token};

        $.post(a_url, data, function(response, status) {
            console.log(status+ ' '+ response);
            var obj = JSON.parse(response);
            if(obj.success == 'true'){
                uname = $('meta[name=user_full_name]').attr("content");
                upic = $('meta[name=user_profile_pic]').attr("content");

                elem = '<li class="comment_item">'+
                        '<div class="comment-meta">'+
                            '<div class="comment-author-info-pic">'+
                              '<img class="profile_photo_img" src="'+upic+'" alt="'+uname+'" height="50" width="50">'+
                            '</div>'+
                            '<div class="comment-author-info-text">'+
                              '<div class="comment-author-info-name">'+
                                 '<span><a href="#">'+uname+'</a></span>'+
                              '</div>'+
                              '<div class="comment-date"><a href="/'+qid+'/answer/'+aid+'#'+obj.cid+'" class="comment-date-link">'+obj.cdate+'</a></div>'+
                            '</div>'+
                        '</div>'+
                        '<div class="comment-content">'+
                            '<p class="comment_text">'+ctext+'</p>'+
                        '</div>'+
                        '<div class="comment-actions">'+
                        '</div>'+
                    '</li>';
                parent_list.find('.comment_list').append(elem).fadeIn(500);
                button.siblings('.user_comment_input').val('');

            }else{
                error_text = obj.error;
                var item = $('<span class="badge badge-warning">'+error_text+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));

            }

        });

        return false;
    });

    $('.bookmark_answer').on('click', function(e){
        e.preventDefault();
        button = $(this)
        aid = button.attr('data-answer');
        action_req = button.attr('data-book-action');

        a_url = '/bookanswer/'+aid+'/'+action_req;
        $.get(a_url, function(data, status) {
            console.log(status+" "+data);
            var obj = JSON.parse(data);
            if(obj.success == 'true'){
                if(obj.action_taken == 'bookmarked'){
                    button.addClass('pressed');
                    button.attr('data-book-action','0')
                }else{
                    button.removeClass('pressed');
                    button.attr('data-book-action','1')
                }
            }else{
                error_text = obj.error;
                var item = $('<span class="badge badge-warning">'+error_text+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));
            }

        });

        return false;
    });

    function removeAutosuggest($elem){
		$elemClone = $elem.clone();
		$elem.parents('ul.as-selections').siblings('.as-results').remove();
		$elem.parents('ul.as-selections').replaceWith($elemClone);
	}

    $('.edit_question_topic').on('click', function(e){
        e.preventDefault()

        qid = $(this).attr('data-qid');
        post_id = $(this).parents('.post_item').attr('id');
        pf = $(this).attr('data-prefill-topics');
        $prefill_value='';
        try{
            $prefill_value = $.parseJSON(pf);
        }catch(e){
            $prefill_value = '';
        }


        removeAutosuggest($('input.topic_search'));
        $('input.topic_search').autoSuggest("/topic_search", {
            asHtmlID: "search-topic",
			queryParam: "aq",
			startText: "",
			resultsHighlight: true,
			selectedItemProp: "name",
			searchObjProps: "name",
			usePlaceholder: true,
			selectionLimit: 5,
			resultsHighlight: true,
			selectionAdded: function(elem){ },
			preFill: $prefill_value,
			formatList: function(data, elem){
                var new_elem = elem.html('<a href="#" data-topic-id="'+data.id+'" ><span style="display: block;">'+data.name+'<span class="user-pic"><img src="" /></span></span><span class="no_of_followers"><span class="number">1000</span> Followers</span></a>');
                return new_elem;

            }

            /*,
            resultsComplete: function(){
                $input_val = $('.add_new_topic input[name="search"]').val();
                $('.add_new_topic .as-list').append('<li class="as-result-item show-all-search"><a target="blank" href="'+encodeURI('/search.php?q='+$input_val)+'">Show All</a></li>');
            }*/
        });
        $('.edit_question_topics_modal').find('input[name="qid"]').val(qid);
        $('.edit_question_topics_modal').find('input[name="post_item"]').val(post_id);
        $('.edit_question_topics_modal').modal('show');
        return false;
    });

    $('.change_question_topic_submit').on('click', function(e){
        e.preventDefault();
        post_id = $('.edit_question_topics_modal').find('input[name="post_item"]').val();
        csrf_token = $('.edit_question_topics_modal').find('input[name="csrfmiddlewaretoken"]').val();
        ts = $('.edit_question_topics_modal').find('input#as-values-search-topic').val();
        qid = $('.edit_question_topics_modal').find('input[name="qid"]').val();
        a_url =  '/edit_question_topics/'+qid;
        data = {'topic_s': ts, csrfmiddlewaretoken: csrf_token};

        $.post(a_url, data, function(response, status) {
            console.log(status+ ' '+ response);
            var obj = JSON.parse(response);
            if(obj.success == true){
                t = '#'+post_id;
                retshow = obj.retshow;
                $(t).find('.edit_question_topic').attr('data-prefill-topics', JSON.stringify(retshow));
                $(t).find('.TopicListItem .item_list').empty();
                for(var key in retshow){
                    console.log(key);
                    ti = '';
                    if(!$(t).find('.TopicListItem').hasClass('type2')) ti = '<span class="bullet">&nbsp;&bull;&nbsp;</span>';
                    ti += '<a class="HoverMenu TopicNameLink topic_name" href="/topic/'+retshow[key]['value']+'">'+
                        '<span class="topic_name_text">'+
                            '<span class="TopicNameSpan TopicName">'+retshow[key]['name']+'</span>'+
                        '</span>'+
                    '</a>';
                    $(t).find('.TopicListItem .item_list').append(ti);
                }

                if(obj.part == true){
                    nf = obj.nf;
                    var item = $('<span class="badge badge-warning">There were '+nf+' topics that we could not find!</span>').hide();
                    $('.sticky-badge').append(item);
                    item.fadeIn(500, runEffect(item));
                }
                $('.edit_question_topics_modal').modal('hide');
            }else{
                error_text = obj.error;
                var item = $('<span class="badge badge-warning">'+error_text+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));

            }
        });
        return false;
    });

    $('.follow_topic, .bookmark_topic').on('click', function(e){
        e.preventDefault();
        button = $(this)
        tid = $(this).attr('data-topic-id');
        ar = $(this).attr('data-action');
        mast = $(this).attr('data-master');
        csrf_token = $(this).find('input[name="csrfmiddlewaretoken"]').val();
        a_url =  '/fb_topic/'+tid+'/'+ar;
        data = {master: mast, csrfmiddlewaretoken: csrf_token};

        $.post(a_url, data, function(response, status) {
            console.log(status+ ' '+ response);
            var obj = JSON.parse(response);
            if(obj.success == true){
                if(obj.action_taken == 1){
                    button.addClass('pressed');
                    button.attr('data-action','0')
                }else{
                    button.removeClass('pressed');
                    button.attr('data-action','1')
                }
                button.find('.action_count').empty().text(obj.count);
            }else{
                error_text = obj.error;
                var item = $('<span class="badge badge-warning">'+error_text+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));

            }
        });
        return false;
    });

    $('.follow_question').on('click', function(e){
        e.preventDefault();
        button = $(this);
        qid = button.attr('data-question');
        action_req = button.attr('data-action');
        csrf_token = button.find('input[name="csrfmiddlewaretoken"]').val();
        a_url = '/follow_question/'+qid+'/'+action_req;
        data = {csrfmiddlewaretoken: csrf_token};

        $.post(a_url, data, function(response, status) {
            console.log(status+ ' '+ response);
            var obj = JSON.parse(response);
            if(obj.success == true){
                if(obj.action_taken == 1){
                    button.addClass('pressed');
                    button.attr('data-action','0')
                }else{
                    button.removeClass('pressed');
                    button.attr('data-action','1')
                }
                button.find('.action_count').empty().text(obj.count);
            }else{
                error_text = obj.error;
                var item = $('<span class="badge badge-warning">'+error_text+'</span>').hide();
                $('.sticky-badge').append(item);
                item.fadeIn(500, runEffect(item));

            }
        });

        return false;
    });


});
