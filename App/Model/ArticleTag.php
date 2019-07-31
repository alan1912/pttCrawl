<?php

namespace M;

class ArticleTag extends Model {
  static $relations = [
      'tags' => '->Tag',
      'articles' => 'Article'
  ];
}
