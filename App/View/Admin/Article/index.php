<?php

use \CRUD\Table\Search\Input    as Input;
use \CRUD\Table\Search\Checkbox as Checkbox;

use \CRUD\Table\Id       as Id;
use \CRUD\Table\Ctrl     as Ctrl;
use \CRUD\Table\Text     as Text;
use \CRUD\Table\Items    as Items;
use \CRUD\Table\Datetime as Datetime;


echo $table->search(function() {

  Input::create('ID')
       ->sql('id = ?');

  Input::create('文章標題')
       ->type('title')
       ->sql('title LIKE ?');
});

echo $table->list(function($obj) {

  Id::create();

  Items::create('標籤')
      ->val(array_map(function($articleTag) {
        return $articleTag->tags->title;
      }, $obj->articleTags));

  Text::create('文章標題')
      ->val($obj->title);

  Datetime::create('新增時間')
          ->align('right')
          ->val($obj->createAt);

  Ctrl::create()->setShowRouter('AdminArticleShow', $obj);
});

echo $table->pages();