<?php

use \CRUD\Show\Id       as Id;
use \CRUD\Show\Text     as Text;
use \CRUD\Show\Datetime as Datetime;

echo $show->back();

echo $show->panel(function($obj) {

  Id::create();

  Text::create('標籤名稱')
       ->val($obj->title);

  Datetime::create('新增時間')
          ->val($obj->createAt);
});