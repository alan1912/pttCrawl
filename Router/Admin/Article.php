<?php

// 首頁 Banner 管理
Router::dir('admin', 'Admin', function() {
  Router::get('article')->controller('Article@index');
  Router::get('article/(id:id)')->controller('Article@show');
});