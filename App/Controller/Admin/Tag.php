<?php

use \CRUD\Form        as Form;
use \CRUD\Show        as Show;
use \CRUD\Table       as Table;
use \CRUD\Table\Order as Order;

class Tag extends AdminController {

  public function __construct() {
    parent::__construct();

    ifErrorTo('AdminTagIndex');

    $this->methodIn('show', function() {
      return $this->obj = \M\Tag::one('id = ?', Router::param('id'));
    });

    $this->view->with('title', '標籤管理')
               ->with('currentMenuUrl', Url::router('AdminTagIndex'));
  }

  public function index() {
    $table = Table::create('\M\Tag', ['order' => Table\Order::desc('id')]);

    return $this->view->with('table', $table);
  }

  public function show() {
    $show = Show::create($this->obj)
                ->setBackRouter('AdminTagIndex');

    return $this->view->with('show', $show);
  }

}