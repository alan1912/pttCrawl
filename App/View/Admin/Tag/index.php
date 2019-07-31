<?php

use \CRUD\Table\Search\Input    as Input;
use \CRUD\Table\Search\Checkbox as Checkbox;

use \CRUD\Table\Id       as Id;
use \CRUD\Table\Ctrl     as Ctrl;
use \CRUD\Table\Text     as Text;
use \CRUD\Table\Datetime as Datetime;


echo $table->search(function() {

  Input::create('ID')
       ->sql('id = ?');

  Input::create('標籤名稱')
       ->type('title')
       ->sql('title LIKE ?');
});

echo $table->list(function($obj) {

  Id::create();

  Text::create('標籤名稱')
      ->val($obj->title);

  Datetime::create('新增時間')
          ->align('right')
          ->val($obj->createAt);

  Ctrl::create()->setShowRouter('AdminTagShow', $obj);
});

echo $table->pages();