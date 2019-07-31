

<button id="crawlBeauty">爬表特版</button>

<script>
  $(function(){
    $('#crawlBeauty').click(function(){
      $("#crawlBeauty").prop("disabled", true)
      $.ajax({
        method: 'POST',
        url: '<?php echo Url::router('AdminCrawlCrawl'); ?>',
        data: {},
        success: function(response) {
          $("#crawlBeauty").prop("disabled", false)
          alert('爬取完畢')
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          $("#crawlBeauty").prop("disabled", false)
          alert('系統異常')
          console.log(JSON.stringify(jqXHR));
          console.log("AJAX error: " + textStatus + ' : ' + errorThrown);
        }
      });
    })
  })
</script>