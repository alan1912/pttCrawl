<?php

use \CRUD\Form        as Form;
use \CRUD\Show        as Show;
use \CRUD\Table       as Table;
use \CRUD\Table\Order as Order;

class Crawl extends AdminController {

  public function __construct() {
    parent::__construct();

    ifErrorTo('AdminCrawlIndex');

    $this->view->with('title', '爬蟲管理')
               ->with('currentMenuUrl', Url::router('AdminCrawlIndex'));
  }

  public function index() {
    // $table = Table::create('\M\Article', ['order' => Table\Order::desc('id')]);

    $table = [];
    return $this->view->with('table', $table);
  }

}