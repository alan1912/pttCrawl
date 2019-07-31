<?php

// 首頁 Banner 管理
Router::dir('admin', 'Admin', function() {
  Router::get('crawl')->controller('Crawl@index');
  Router::post('crawl/crawl')->controller('Crawl@crawl');
});