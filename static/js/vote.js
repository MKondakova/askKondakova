$('.rating').each(function (ev) {
    const rating_field = $(this).find('.rating-field');
    const btns = $(this).find('.js-vote-btn');
    btns.click(function (ev) {
        ev.preventDefault();
        const $this = $(this),
            action = $this.data('action'),
            rate_object_id = $this.data('qid'),
            object_type = $this.data('type');
        $.ajax('/vote/', {
            method: 'POST',
            data: {action: action, rate_object_id: rate_object_id, object_type: object_type},
            dataType: "json",
            error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.responseText);
            },
            success: function (data) {
                if (data['redirect']) {
                    console.log(data['redirect'])
                    window.location = data['redirect'];
                } else {
                    if ($this.hasClass('selected')) {
                        $this.removeClass('selected')
                    } else {
                        btns.removeClass('selected')
                        $this.addClass('selected')
                    }
                    rating_field.html(data.qrating);
                }
            },
        });
    });

})