<?php

use \CRUD\Form        as Form;
use \CRUD\Show        as Show;
use \CRUD\Table       as Table;
use \CRUD\Table\Order as Order;

class Article extends AdminController {

  public function __construct() {
    parent::__construct();

    ifErrorTo('AdminArticleIndex');

    $this->methodIn('show', function() {
      return $this->obj = \M\Article::one('id = ?', Router::param('id'));
    });

    $this->view->with('title', '文章管理')
               ->with('currentMenuUrl', Url::router('AdminArticleIndex'));
  }

  public function index() {
    $table = Table::create('\M\Article', ['order' => Table\Order::desc('id')]);

    return $this->view->with('table', $table);
  }

  public function show() {
    // foreach (\M\ArticleImage::all(['where' => ['articleId = ?', $this->obj->id]]) as $images) {
    //   if (preg_match("/https?/", $images->img)) {
    //     $images->img->putUrl($images->img);
    //   }
    // }

    $show = Show::create($this->obj)
                ->setBackRouter('AdminArticleIndex');

    return $this->view->with('show', $show);
  }

}