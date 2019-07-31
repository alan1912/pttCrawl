<?php

use \CRUD\Show\Id       as Id;
use \CRUD\Show\Text     as Text;
use \CRUD\Show\Datetime as Datetime;
use \CRUD\Show\Image    as Image;

echo $show->back();

echo $show->panel(function($obj) {

  Id::create();

  Text::create('文章標題')
       ->val($obj->title);

  foreach (\M\ArticleImage::all(['where' => ['articleId = ?', $obj->id]]) as $key => $images) {
    $num = ($key+1);
    Image::create('圖片'.$num)
         ->val($images->img);
  }

  Datetime::create('新增時間')
          ->val($obj->createAt);
});