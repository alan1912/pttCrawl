<?php

namespace M;

class Article extends Model {
  static $relations = [
    'articleTags' => 'ArticleTag',
    'crawlUrl' => '->CrawlUrl',
  ];
}
