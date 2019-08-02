$(function(){
    $('#crawlBeauty').click(function(){
      var that = $(this)
      that.prop("disabled", true)
      $.ajax({
        method: 'POST',
        url: that.data('url'),
        data: {},
        success: function(response) {
          that.prop("disabled", false)
          alert('爬取完畢: 此次爬取 ' + response['messages'][0] + ' 筆文章')
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          that.prop("disabled", false)
          alert('系統異常')
          console.log(JSON.stringify(jqXHR));
          console.log("AJAX error: " + textStatus + ' : ' + errorThrown);
        }
      });
    })
  })