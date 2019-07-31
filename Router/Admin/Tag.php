<?php

// 首頁 Banner 管理
Router::dir('admin', 'Admin', function() {
  Router::get('tag')->controller('Tag@index');
  Router::get('tag/(id:id)')->controller('Tag@show');
});