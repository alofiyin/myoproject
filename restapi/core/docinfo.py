#_*_coding:utf-8_*_
#api说明信息
server_info= {
    "swagger": "2.0",
    "info": {
        "description": "这是一个数据rest api .用于测试。",
        "version": "1.0.0",
        "title": "rest api",
        "termsOfService": "http://swagger.io/terms/",
        "contact": {
            "email": "alofiyin@gmail.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    },
    "host": "192.168.10.126:8010",
    "basePath": "/1.0",
    "externalDocs": {
        "description": "遵循http1.1协议",
        "url": "http://swagger.io"
    },
   "tags":[],
    "schemes": [
        "http"
    ],
    "paths": {},
    #安全检测设置
    "securityDefinitions": {
        "api_key": {
            "type": "apiKey",
            "name": "api_key",
            "in": "header"
        }
    },
    #定义数据结构
    "definitions": {
        "Dbo": {
            "type": "object",
            "required": [

            ],
            "properties": {
								"field1":{
										"type": "string"
								},
								"field2":{
										"type": "string"
								},
								"field3":{
									"type": "string"
								}
            }
        },
        "ResDataBody":{
        	"type": "object",
        	"properties":{
        				"result":{
        						"type": "array",
        						"items":{
        									"type": "object",
        									"properties":{
        												"field1":{
        														"type": "string"
        												}
        									}
        						}
        				}
		
        	}
        },
        "ResDict":{
        	"type": "object",
        	"properties":{
        				"result":{
        						"title": "object"
        				}		
        	}
        },
        "ResInt":{
        	"type": "object",
        	"properties":{
        				"result":{
        						"type": "integer",
        						 "format": "int32"
        				}
		
        	}
        }
    },      	 
}
consumes_style= ["application/json"]
produces_style= ["application/json"]
#返回状态样式
responses_style= {
		          "200": {
		               "description": "返回记录的结果集",
		               "schema": {
							"$ref": "#/definitions/ResDataBody"
		               }
		          },
		          "400": {
		               "description": "返回错误信息说明"
		          },
		          "404": {
		               "description": "path not found"
		          }
}
#tags样式
tags_style =  {
            "name": "search",
            "description": "搜索引擎操作",
            "externalDocs": {
                "description": "Find out more about our store",
                "url": "http://swagger.io"
            }
}
#搜索引擎样式
sphinx_style = {
    "/search/{index}":{
		"get":{
		    "tags": ["search"],
		    "summary": "搜索服务",
		    "description": "提交搜索条件获取搜索结果",
		    #参数设置
		    "parameters": [
		    	{
		           "name": "index",
		           "in": "path",
		           "description": "搜索引擎索引标识",
		           "required": True,
		           "type": "string"                      	
		    	},
		    	{
		           "name": "keyw",
		           "in": "query",
		           "description": "要搜索的关键词",
		           "required": False,
		           "type": "string"                  	
		    	},           
		        {
		           "name": "fields",
		           "in": "query",
		           "description": "返回的数据表字段名 多个字段以(,)分隔",
		           "required": False,
		           "type": "string"
		        },
		        {
		           "name": "opt",
		           "in": "query",
		           "description": "筛选条件设置，格式 字段名:值;字段名:值",
		           "required": False,
		           "type": "string"
		        },     
		        {
		           "name": "order",
		           "in": "query",
		           "description": "排序字段 参数sql的order by 语法",
		           "required": False,
		           "type": "string"
		        },
		        {
		           "name": "group",
		           "in": "query",
		           "description": "分组设置",
		           "required": False,
		           "type": "string"
		        }, 
		        {
		           "name": "page",
		           "in": "query",
		           "description": "页码 默认为1",
		           "required": False,
		           "type": "string"
		        },      
		        {
		           "name": "pagesize",
		           "in": "query",
		           "description": "每页记录数 默认为20",
		           "required": False,
		           "type": "string"
		        }          
		     ],
		     #返回状态设置
		     "responses": {
		          "200": {
		               "description": "返回记录的结果集",
		               "schema": {
							"$ref": "#/definitions/ResDataBody"
		               }
		          }
		     }
		}
	}
}
#数据库写操作样式
dbo_style = {
	"path":"/dbo/{dbname}/{table}",
	"operation":{
        "post": {
           "tags": [
               "DBOperation"
           ],
          "summary": "新增一条记录",
          "description": "往数据库{dbname}表{table}插入一条记录",
           "parameters": [
               {
                   "name": "dbname",
                   "in": "path",
                   "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                   "required": True,
                   "type": "string"                      	
               },
               {
                   "name": "table",
                   "in": "path",
                   "description": "数据表名",
                   "required": True,
                   "type": "string"                  	
               },
               {
                   "in": "body",
                   "name": "body",
                   "description": "记录的内容 json格式",
                   "required": True,
                   "schema": {
                       "$ref": "#/definitions/Dbo"
                   }
               }
               
           ],
           "responses": {
               "200": {
                   "description": "返回记录的入库id编号",
                   "schema": {
										"$ref": "#/definitions/ResInt"
                   }
               }
            }
       },
       "put": {
            "tags": [
                    "DBOperation"
             ],
             "summary": "更新一条已成存的记录",
             "description": "更新数据库{dbname}表{table}中已存在的一条记录",
             "parameters": [
                 {
                     "name": "dbname",
                     "in": "path",
                     "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                     "required": True,
                     "type": "string"                      	
                 },
                 {
                     "name": "table",
                     "in": "path",
                     "description": "数据表名",
                     "required": True,
                     "type": "string"                  	
                 },           
                 {
                     "in": "body",
                     "name": "body",
                     "description": "要更新的记录字段与值，必须包含id字段",
                     "required": True,
                     "schema": {
                         "$ref": "#/definitions/Dbo"
                     }
                 }
             ],
             "responses": {
                 "200": {
                     "description": "返回受影响的记录条数",
                     "schema": {
														"$ref": "#/definitions/ResInt"
                     }
                 }                  
             }
        },
        "delete": {
            "tags": [
                "DBOperation"
            ],
            "summary": "删除一条/多条已成存在的记录",
            "description": "删除数据库{dbname}表{table}中已存在的一条/多条记录,公司、产品、 资讯表暂不支持多条删除",
            "parameters": [
                {
                    "name": "dbname",
                    "in": "path",
                    "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                    "required": True,
                    "type": "string"                      	
                },
                {
                    "name": "table",
                    "in": "path",
                    "description": "数据表名",
                    "required": True,
                    "type": "string"                  	
                },           
                {
                    "name": "id",
                    "in": "query",
                    "description": "需要删除的记录id,多个id以(,)分隔 ",
                    "required": True,
                    "type": "string"
                }
            ],
            "responses": {
                "200": {
                    "description": "返回受影响的记录条数",
                    "schema": {
										"$ref": "#/definitions/ResInt"
                    }
                }
            }
        },
        "get": {
            "tags": [
                "dbquery"
            ],
            "summary": "查询记录",
            "description": "查询数据库{dbname}表{table}中的记录",
            "parameters": [
                {
                    "name": "dbname",
                    "in": "path",
                    "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                    "required": True,
                    "type": "string"                      	
                },
                {
                    "name": "table",
                    "in": "path",
                    "description": "数据表名",
                    "required": True,
                    "type": "string"                  	
                },           
                {
                    "name": "fields",
                    "in": "query",
                    "description": "需要返回的字段名 多个字段以(,)分隔",
                    "required": False,
                    "type": "string"
                },
                {
                    "name": "where",
                    "in": "query",
                    "description": "查询条件 参数sql的where语法",
                    "required": False,
                    "type": "string"
                },
                {
                    "name": "order",
                    "in": "query",
                    "description": "排序字段 参数sql的order by 语法",
                    "required": False,
                    "type": "string"
                },
                 {
                    "name": "group",
                    "in": "query",
                    "description": "分组字段 参数sql的group by 语法",
                    "required": False,
                    "type": "string"
                }, 
                 {
                    "name": "page",
                    "in": "query",
                    "description": "页码 默认为1",
                    "required": False,
                    "type": "string"
                },      
                 {
                    "name": "pagesize",
                    "in": "query",
                    "description": "每页记录数 默认为20",
                    "required": False,
                    "type": "string"
                }           
                ],
           "responses": {
               "200": {
                   "description": "返回受影响的记录条数",
                   "schema": {
														"$ref": "#/definitions/ResDataBody"
                   }
               }
           }
        }
    }
}   
dbquery_style={
    "/dbo/{dbname}/{table}/getbyid": {
        "get": {
            "tags": [
                "dbquery"
            ],
            "summary": "根据id提取记录",
            "description": "根据记录id提取数据库{dbname}表{table}中的记录",
            "parameters": [
                {
                    "name": "dbname",
                    "in": "path",
                    "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                    "required": True,
                    "type": "string"                      	
                },
                {
                    "name": "table",
                    "in": "path",
                    "description": "数据表名",
                    "required": True,
                    "type": "string"                  	
                },           
                {
                    "name": "fields",
                    "in": "query",
                    "description": "需要返回的字段名 多个字段以(,)分隔",
                    "required": False,
                    "type": "string"
                },
    
                 {
                    "name": "ids",
                    "in": "query",
                    "description": "记录的id编号 多个id以(,)分隔",
                    "required": True,
                    "type": "string"
                }           
            ],
            "responses": {
                "200": {
                    "description": "返回记录的结果集",
                    "schema": {
			"$ref": "#/definitions/ResDataBody"
                    }
                } 
            }
        }
    },
    "/dbo/{dbname}/{table}/getcount": {
        "get": {
            "tags": [
                "dbquery"
            ],
            "summary": "查询记录数量",
            "description": "查询数据库{dbname}表{table}中符合条件的的记录条数",
            "parameters": [
                {
                    "name": "dbname",
                    "in": "path",
                    "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                    "required": True,
                    "type": "string"                      	
                },
                {
                    "name": "table",
                    "in": "path",
                    "description": "数据表名",
                    "required": True,
                    "type": "string"                  	
                },               
                {
                    "name": "where",
                    "in": "query",
                    "description": "查询条件 参数sql的where语法",
                    "required": False,
                    "type": "string"
                }         
            ],
            "responses": {
                "200": {
                    "description": "返回记录条数",
                    "schema": {
			"$ref": "#/definitions/ResInt"
                    }
                }
            }
        }
    },
    "/dbo/{dbname}/{table}/getlist": {
        "get": {
            "tags": [
                "dbquery"
            ],
            "summary": "获取记录列表",
            "description": "获取数据库{dbname}表{table}中符合条件的的记录列表",
            "parameters": [
                {
                    "name": "dbname",
                    "in": "path",
                    "description": "数据库简写标识[com,prod,home,buy,news,help,price,zhaoshang,expo]",
                    "required": True,
                    "type": "string"                      	
                },
                {
                    "name": "table",
                    "in": "path",
                    "description": "数据表名",
                    "required": True,
                    "type": "string"                  	
                },               
                  {
                    "name": "fields",
                    "in": "query",
                    "description": "需要返回的字段名 多个字段以(,)分隔",
                    "required": False,
                    "type": "string"
                },
                {
                    "name": "where",
                    "in": "query",
                    "description": "查询条件 参数sql的where语法",
                    "required": False,
                    "type": "string"
                },
                {
                    "name": "order",
                    "in": "query",
                    "description": "排序字段 参数sql的order by 语法",
                    "required": False,
                    "type": "string"
                }, 
                 {
                    "name": "page",
                    "in": "query",
                    "description": "页码 默认为1",
                    "required": False,
                    "type": "string"
                },      
                 {
                    "name": "pagesize",
                    "in": "query",
                    "description": "每页记录数 默认为20",
                    "required": False,
                    "type": "string"
                }           
            ],
            "responses": {
                "200": {
                    "description": "返回受影响的记录条数",
                    "schema": {
										"$ref": "#/definitions/ResDataBody"
                    }
                }
            }
        }
    }
}
#业务接口
biz_api={
	#公司相关接口
        "/query/comcorp/getbyname": {
            "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据公司名称获取对应的信息",
                "description": "根据公司名称获取对应的信息",
                "parameters": [
                     {
                        "name": "com_name",
                        "in": "query",
                        "description": "公司名称",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },
        "/query/comcorp/getbydomain": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据公司三级域名获取对应的信息",
                "description": "根据公司三级域名获取对应的信息",
                "parameters": [
                     {
                        "name": "domain",
                        "in": "query",
                        "description": "公司三级域名",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },
        "/query/comcorp/getbyuserid": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据用户id获取一条公司的信息",
                "description": "根据用户id获取一条公司的信息",
                "parameters": [
                     {
                        "name": "user_id",
                        "in": "query",
                        "description": "用户id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },
        "/query/comcorp/getlistbyuserid": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据用户id获取公司的信息列表",
                "description": "根据用户id获取公司的信息列表",
                "parameters": [
                     {
                        "name": "user_id",
                        "in": "query",
                        "description": "用户id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },  
        "/query/comcorp/gettagbycomid": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据公司id获取一条公司标签关联值",
                "description": "根据公司id获取一条公司标签关联值",
                "parameters": [
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        }, 
        "/query/comcorp/getkeywbycomid": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "根据公司id获取公司展厅关键字",
                "description": "根据公司id获取公司展厅关键字",
                "parameters": [
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }          
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },                  
        "/query/comcorp/getmaxid": {
             "get": {
                "tags": [
                    "ComInfo"
                ],
                "summary": "获取公司的最大ID",
                "description": "获取公司表的最大记录ID号",
                "parameters": [
        
                ],
                "responses": {
                    "200": {
                        "description": "返回最大id号",
                        "schema": {
							"$ref": "#/definitions/ResInt"
                        }
                    }
                }
            }
        },
	#产品相关接口
        "/query/prodinfo/getgroupbycomid": {
             "get": {
                "tags": [
                    "ProInfo"
                ],
                "summary": "根据公司ID获取统计列表",
                "description": "根据公司ID获取统计列表",
                "parameters": [   
                     {
                        "name": "group",
                        "in": "query",
                        "description": "分组字段名 默认status",
                        "required": False,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回group字段的值与统计数num",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },
        "/query/prodinfo/getlistbycomid": {
             "get": {
                "tags": [
                    "ProInfo"
                ],
                "summary": "根据公司ID获取产品列表",
                "description": "根据公司ID获取产品列表",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    },     
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "where",
                        "in": "query",
                        "description": "查询条件 参数sql的where语法",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "order",
                        "in": "query",
                        "description": "排序字段 参数sql的order by 语法",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "page",
                        "in": "query",
                        "description": "页码 默认为1",
                        "required": False,
                        "type": "string"
                    },      
                     {
                        "name": "pagesize",
                        "in": "query",
                        "description": "每页记录数 默认为20",
                        "required": False,
                        "type": "string"
                    }  
                ],
                "responses": {
                    "200": {
                        "description": "返回记录结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },
        "/query/prodinfo/getcountbycomid": {
             "get": {
                "tags": [
                    "ProInfo"
                ],
                "summary": "根据公司ID获取产品列表数量",
                "description": "根据公司ID获取产品列表数量",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数量",
                        "schema": {
							"$ref": "#/definitions/ResInt"
                        }
                    } 
                }
            }
        },
        "/query/prodinfo/getlistbyname": {
             "get": {
                "tags": [
                    "ProInfo"
                ],
                "summary": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "description": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "parameters": [   
                     {
                        "name": "title",
                        "in": "query",
                        "description": "产品标题",
                        "required": True,
                        "type": "string"
                    },
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "rettype",
                        "in": "query",
                        "description": "返回信息类型,0返回数字,1返回重复的数据,默认为0",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "fields",
                        "in": "query",
                        "description": "字段名, 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }                
                ],
                "responses": {
                    "200": {
                        "description": "status不存在返回1,存在返回2|data 记录集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },

   #产口标签相关接口

        "/query/prodtag/getroottag": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "获取一级标签信息",
                "description": "获取一级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/prodtag/getsecondtag": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "获取二级标签信息",
                "description": "获取二级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/prodtag/getsubtag": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "获取一级标签的所有子类",
                "description": "获取一级标签的所有子类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/prodtag/getcurrentsubtag": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "获取当前标签的下一级分类",
                "description": "获取当前标签的下一级分类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/prodtag/getbytagid": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "根据tag_id获取对应的标签信息",
                "description": "根据tag_id获取对应的标签信息",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id 多个id以(,)分隔",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        }, 
        "/query/prodtag/gettagbykeyw": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "根据名称查找对应的标签信息",
                "description": "根据名称查找对应的标签信息",
                "parameters": [ 
                     {
                        "name": "name",
                        "in": "query",
                        "description": "标签名称",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },   
        "/query/prodtag/gettagsbynames": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "根据标签名称列表获取产品标签ID",
                "description": "根据标签名称列表获取产品标签ID",
                "parameters": [ 
                     {
                        "name": "name",
                        "in": "query",
                        "description": "标签名称 多个标签以(.)分配",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        }, 
        "/query/prodtag/gettagsbynames": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "获取标签信息(所有或者一级或者id名称对应信息)",
                "description": "获取标签信息(所有或者一级或者id名称对应信息)",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id :0 显示所有标签,1 显示一级标签,2 就显示二级标签,tag_id=101,102显示tag_id=>名称对应的标签数组",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }                 
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        }, 
        "/query/keywrelate/getletter": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "根据字母字符串查找相关关键字",
                "description": "根据字母字符串查找相关关键字",
                "parameters": [ 
                     {
                        "name": "letters",
                        "in": "query",
                        "description": "关键字的字母字符串",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 
        "/query/keywrelate/getbyname": {
             "get": {
                "tags": [
                    "ProTag"
                ],
                "summary": "根据关键字查找相关关键字",
                "description": "根据关键字查找相关关键字(产品、公司、网址、求购)",
                "parameters": [ 
                     {
                        "name": "keyw",
                        "in": "query",
                        "description": "关键字",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
	#用户相关接口
        "/query/userinfo/getbyname": {
             "get": {
                "tags": [
                    "UserInfo"
                ],
                "summary": "根据帐号获取一条用户帐号信息",
                "description": "根据帐号获取一条用户帐号信息",
                "parameters": [ 
                     {
                        "name": "name",
                        "in": "query",
                        "description": "用户账号",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 
        "/query/userinfo/getinfobyemail": {
             "get": {
                "tags": [
                    "UserInfo"
                ],
                "summary": "根据邮箱获取一条用户帐号信息",
                "description": "根据邮箱获取一条用户帐号信息",
                "parameters": [ 
                     {
                        "name": "name",
                        "in": "query",
                        "description": "用户账号",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/usercorpfile/getcachebyuserid": {
             "get": {
                "tags": [
                   "UserInfo"
                ],
                "summary": "根据会员ID获取公司档案缓存信息",
                "description": "根据会员ID获取公司档案缓存信息",
                "parameters": [ 
                     {
                        "name": "user_id",
                        "in": "query",
                        "description": "会员ID",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },

    #通用业务接口
        "/query/common/getroottag": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取一级标签信息",
                "description": "获取一级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/common/getsecondtag": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取二级标签信息",
                "description": "获取二级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/common/getrootsecondtag": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取一、二级标签信息(省份、城市)",
                "description": "获取一、二级标签信息(省份、城市)",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/common/getcurrentsubtag": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取当前标签的下一级分类",
                "description": "获取当前标签的下一级分类",
                "parameters": [ 
                     {
                        "name": "sortid",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 
        "/query/common/getbytagid": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "根据sortid获取对应的标签信息",
                "description": "根据sortid获取对应的标签信息",
                "parameters": [ 
                     {
                        "name": "sortid",
                        "in": "query",
                        "description": "标签id 多个id以(,)分隔",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 
        "/query/common/gettags": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取省份标签信息(所有或者一级或者id名称对应信息)",
                "description": "获取省份标签信息(所有或者一级或者id名称对应信息)",
                "parameters": [ 
                     {
                        "name": "sortid",
                        "in": "query",
                        "description": "标签id :0 显示所有标签,1 显示一级标签,2 就显示二级标签,tag_id=101,102显示sortid=>名称对应的标签数组",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }                 
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },

     #展会标签相关接口
        "/query/common/getexpotags": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取展会标签信息(所有或者一级或者id名称对应信息)",
                "description": "获取展会标签信息(所有或者一级或者id名称对应信息)",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id :0 显示所有标签,1 显示一级标签,2 就显示二级标签,tag_id=101,102显示sortid=>名称对应的标签数组",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }                 
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 
        "/query/common/getexopsubtag": {
             "get": {
                "tags": [
                    "Common"
                ],
                "summary": "获取展会一级标签的所有子类",
                "description": "获取展会一级标签的所有子类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        }, 

     #招商相关接口
        "/query/zsinfo/getgroupbycomid": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "根据公司ID获取统计列表",
                "description": "根据公司ID获取统计列表",
                "parameters": [   
                     {
                        "name": "group",
                        "in": "query",
                        "description": "分组字段名 默认status",
                        "required": False,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回group字段的值与统计数num",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },
        "/query/zsinfo/getcount": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取公司招商列表数量",
                "description": "获取公司招商列表数量",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数量",
                        "schema": {
							"$ref": "#/definitions/ResInt"
                        }
                    }
                }
            }
        },  
        "/query/zsinfo/getlistbycomid": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "根据公司ID获取产品列表",
                "description": "根据公司ID获取产品列表",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    },     
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "where",
                        "in": "query",
                        "description": "查询条件 参数sql的where语法",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "order",
                        "in": "query",
                        "description": "排序字段 参数sql的order by 语法",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "page",
                        "in": "query",
                        "description": "页码 默认为1",
                        "required": False,
                        "type": "string"
                    },      
                     {
                        "name": "pagesize",
                        "in": "query",
                        "description": "每页记录数 默认为20",
                        "required": False,
                        "type": "string"
                    }  
                ],
                "responses": {
                    "200": {
                        "description": "返回记录结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },

     #招商标签直关接口
  
        "/query/zstag/getroottag": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取一级标签信息",
                "description": "获取一级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/zstag/getsecondtag": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取二级标签信息",
                "description": "获取二级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/zstag/getsubtag": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取一级标签的所有子类",
                "description": "获取一级标签的所有子类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/zstag/getcurrentsubtag": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取当前标签的下一级分类",
                "description": "获取当前标签的下一级分类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },
        "/query/zstag/getbytagid": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "根据tag_id获取对应的标签信息",
                "description": "根据tag_id获取对应的标签信息",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id 多个id以(,)分隔",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    } 
                }
            }
        },  
        "/query/zstag/gettags": {
             "get": {
                "tags": [
                    "ZsInfo"
                ],
                "summary": "获取所有标签信息",
                "description": "所有获取标签信息",
                "parameters": [ 
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数据列表",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },

     #求购相关接口

        "/query/buyinfo/getgroupbycomid": {
             "get": {
                "tags": [
                    "BuyInfo"
                ],
                "summary": "根据公司ID获取统计列表",
                "description": "根据公司ID获取统计列表",
                "parameters": [
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    },                   	   
                     {
                        "name": "group",
                        "in": "query",
                        "description": "分组字段名 默认status",
                        "required": False,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回group字段的值与统计数num",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },   
        "/query/buyinfo/getlistbycomid": {
             "get": {
                "tags": [
                    "BuyInfo"
                ],
                "summary": "根据公司ID获取列表",
                "description": "根据公司ID获取列表",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    },     
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "where",
                        "in": "query",
                        "description": "查询条件 参数sql的where语法",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "order",
                        "in": "query",
                        "description": "排序字段 参数sql的order by 语法",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "page",
                        "in": "query",
                        "description": "页码 默认为1",
                        "required": False,
                        "type": "string"
                    },      
                     {
                        "name": "pagesize",
                        "in": "query",
                        "description": "每页记录数 默认为20",
                        "required": False,
                        "type": "string"
                    }  
                ],
                "responses": {
                    "200": {
                        "description": "返回记录结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },
        "/query/buyinfo/getcountbycomid": {
             "get": {
                "tags": [
                    "BuyInfo"
                ],
                "summary": "根据公司ID获取列表数量",
                "description": "根据公司ID获取列表数量",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数量",
                        "schema": {
							"$ref": "#/definitions/ResInt"
                        }
                    }
                }
            }
        },
        "/query/buyinfo/getlistbyname": {
             "get": {
                "tags": [
                    "BuyInfo"
                ],
                "summary": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "description": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "parameters": [   
                     {
                        "name": "title",
                        "in": "query",
                        "description": "标题",
                        "required": True,
                        "type": "string"
                    },   
                    {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": False,
                        "type": "string"
                    }                       
                ],
                "responses": {
                    "200": {
                        "description": "status 不存在返回1,存在返回2,data 数据",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },

     #资讯相关接口

        "/query/newsinfo/getgroupbycomid": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据公司ID获取统计列表",
                "description": "根据公司ID获取统计列表",
                "parameters": [   
                     {
                        "name": "group",
                        "in": "query",
                        "description": "分组字段名 默认status",
                        "required": False,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回group字段的值与统计数num",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },
        "/query/newsinfo/getinfobynewsid": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据资讯ID获取一条资讯推荐信息信息",
                "description": "根据资讯ID获取一条资讯推荐信息信息",
                "parameters": [   
                     {
                        "name": "news_id",
                        "in": "query",
                        "description": "资讯ID",
                        "required": True,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回数据集合",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        },          
        "/query/newsinfo/getlistbyname": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "description": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "parameters": [   
                     {
                        "name": "title",
                        "in": "query",
                        "description": "标题",
                        "required": True,
                        "type": "string"
                    },   
                    {
                        "name": "author",
                        "in": "query",
                        "description": "公司名称",
                        "required": False,
                        "type": "string"
                    }                       
                ],
                "responses": {
                    "200": {
                        "description": "status 不存在返回1,存在返回2,data 数据",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    }
                }
            }
        }, 
        "/query/newsinfo/getlistbycomid": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据公司ID获取记录列表",
                "description": "根据公司ID获取记录列表",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    },     
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "where",
                        "in": "query",
                        "description": "查询条件 参数sql的where语法",
                        "required": False,
                        "type": "string"
                    },
                    {
                        "name": "order",
                        "in": "query",
                        "description": "排序字段 参数sql的order by 语法",
                        "required": False,
                        "type": "string"
                    },
                     {
                        "name": "page",
                        "in": "query",
                        "description": "页码 默认为1",
                        "required": False,
                        "type": "string"
                    },      
                     {
                        "name": "pagesize",
                        "in": "query",
                        "description": "每页记录数 默认为20",
                        "required": False,
                        "type": "string"
                    }  
                ],
                "responses": {
                    "200": {
                        "description": "返回记录结果集",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },
        "/query/newsinfo/getcountbycomid": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据公司ID获取记录列表数量",
                "description": "根据公司ID获取记录列表数量",
                "parameters": [   
                     {
                        "name": "com_id",
                        "in": "query",
                        "description": "公司id",
                        "required": True,
                        "type": "string"
                    }     
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数量",
                        "schema": {
							"$ref": "#/definitions/ResInt"
                        }
                    }
                }
            }
        },  
        "/query/newsinfo/getlistbyname": {
             "get": {
                "tags": [
                    "NewsInfo"
                ],
                "summary": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "description": "根据标题或标题+公司名称判断是否有重复值(多条信息)",
                "parameters": [   
                     {
                        "name": "title",
                        "in": "query",
                        "description": "标题",
                        "required": True,
                        "type": "string"
                    },   
                    {
                        "name": "author",
                        "in": "query",
                        "description": "公司名称",
                        "required": False,
                        "type": "string"
                    }                       
                ],
                "responses": {
                    "200": {
                        "description": "status 不存在返回1,存在返回2,data 数据",
                        "schema": {
							"$ref": "#/definitions/ResDataBody"
                        }
                    } 
                }
            }
        },

    #资讯标签相关接口

        "/query/newstag/getroottag": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "获取一级标签信息",
                "description": "获取一级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/newstag/getsecondtag": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "获取二级标签信息",
                "description": "获取二级标签信息",
                "parameters": [   
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/newstag/getsubtag": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "获取一级标签的所有子类",
                "description": "获取一级标签的所有子类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/newstag/getcurrentsubtag": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "获取当前标签的下一级分类",
                "description": "获取当前标签的下一级分类",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回标签字典",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        },
        "/query/newstag/getbytagid": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "根据tag_id获取对应的标签信息",
                "description": "根据tag_id获取对应的标签信息",
                "parameters": [ 
                     {
                        "name": "tag_id",
                        "in": "query",
                        "description": "标签id 多个id以(,)分隔",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录的结果集",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        }, 
        "/query/newstag/gettags": {
             "get": {
                "tags": [
                    "NewsTag"
                ],
                "summary": "获取所有标签信息",
                "description": "所有获取标签信息",
                "parameters": [ 
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "需要返回的字段名 多个字段以(,)分隔",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "返回记录数据列表",
                        "schema": {
							"$ref": "#/definitions/ResDict"
                        }
                    }
                }
            }
        } 
    
}

#数据表操作列表
table_tag={
	"com":{
			"com_corp":{
				"tag":"ComInfo",
				"title":"公司",
				"description":"",
				"exception":["getlist"]
			},
			"com_corp_check":{
				"tag":"ComInfo",
				"title":"公司审核",
				"description":"	where 语句的可用条件字段id, status, com_name, user_id, domain",
				"exception":[]
			},
			"com_tag_relate":{
				"tag":"ComInfo",
				"title":"公司标签关联值",
				"description":"",
				"exception":["getlist"]
			},
			"com_keyword":{
				"tag":"ComInfo",
				"title":"公司展厅关键字",
				"description":"",
				"exception":["getlist"]
			},
			"com_photo_album":{
				"tag":"ComAlbum",
				"title":"公司相册",
				"description":"",
				"exception":[]
			},
			"com_photos":{
				"tag":"ComAlbum",
				"title":"公司相册图片",
				"description":"",
				"exception":[]
			},
			"com_friend_link":{
				"tag":"ComFriendLink",
				"title":"公司友情链接",
				"description":"",
				"exception":[]
			},
			"com_news":{
				"tag":"ComNews",
				"title":"公司动态",
				"description":"",
				"exception":[]
			},	
			"com_cert":{
				"tag":"ComCert",
				"title":"公司证书",
				"description":"",
				"exception":[]
			},
			"com_blacklist":{
				"tag":"ComBackWarn",
				"title":"公司黑名单、警告",
				"description":"",
				"exception":[]
			},		
			"com_illegal_recode":{
				"tag":"ComIllegalreCode",
				"title":"公司违法记录",
				"description":"",
				"exception":[]
			},	
			"com_setting":{
				"tag":"ComSetting",
				"title":"公司设置",
				"description":"",
				"exception":[]
			},
			"com_tpl":{
				"tag":"ComTpl",
				"title":"公司模板",
				"description":"",
				"exception":[]
			},
			"com_tpl_tag":{
				"tag":"ComTpl",
				"title":"公司模板标签",
				"description":"",
				"exception":[]
			}
		},
		"prod":{
			"pro_info":{
				"tag":"ProInfo",
				"title":"产品",
				"description":"",
				"exception":["getlist"]
			},
			"pro_tag":{
				"tag":"ProTag",
				"title":"产品标签",
				"description":"",
				"exception":["getlist"]
			},
			"pro_tag_attr":{
				"tag":"ProAttr",
				"title":"产品标签属性",
				"description":"",
				"exception":["getlist"]
			},
			"pro_tag_attr_val":{
				"tag":"ProAttr",
				"title":"产品标签属性值",
				"description":"",
				"exception":["getlist"]
			},
			"pro_tag_match":{
				"tag":"ProInfo",
				"title":"产品爬虫标签对应",
				"description":"",
				"exception":["getlist"]
			},
			"pro_picture_relate":{
				"tag":"ProInfo",
				"title":"产品图片关联",
				"description":"",
				"exception":[]
			},
			"pro_picture_relate":{
				"tag":"KeywRelate",
				"title":"产品相关关键字",
				"description":"",
				"exception":[]
			},
			"pro_keyword_stat_cache":{
				"tag":"ProKeywStatCache",
				"title":"关键字缓存统计",
				"description":"",
				"exception":[]
			},
			"pro_news_relate":{
				"tag":"ProKeywStatCache",
				"title":"产品资讯信息关联",
				"description":"",
				"exception":[]
			}			
		},
		"zhaoshang":{
			"zs_info":{
				"tag":"ZsInfo",
				"title":"招商",
				"description":"",
				"exception":[]
			},
			"zs_picture_relate":{
				"tag":"ZsInfo",
				"title":"招商图片关联",
				"description":"",
				"exception":[]
			},
			"zs_tag":{
				"tag":"ZsTag",
				"title":"招商标签",
				"description":"",
				"exception":[]
			}
		},
		"buy":{
			"buy_info":{
				"tag":"BuyInfo",
				"title":"求购",
				"description":"",
				"exception":["getlist"]
			}		
		},
		"news":{
			"news_info":{
				"tag":"NewsInfo",
				"title":"资讯",
				"description":"",
				"exception":["getlist"]
			},	
			"news_tag_match":{
				"tag":"NewsInfo",
				"title":"爬虫标签对应",
				"description":"",
				"exception":["getlist"]
			},	
			"news_picture_relate":{
				"tag":"NewsInfo",
				"title":"资讯图片关联",
				"description":"",
				"exception":[]
			},
			"news_tag_info":{
				"tag":"NewsTag",
				"title":"资讯标签",
				"description":"",
				"exception":["getlist"]
			},	
			"news_rec_info":{
				"tag":"NewsTag",
				"title":"资讯推荐信息",
				"description":"",
				"exception":[]
			}
		},
		"expo":{
			"expo_info":{
				"tag":"ExpoInfo",
				"title":"展会",
				"description":"",
				"exception":["getlist"]	
			},	
			"expo_hall":{
				"tag":"ExpoInfo",
				"title":"展馆",
				"description":"",
				"exception":[]	
			},	
			"expo_hall_picture":{
				"tag":"ExpoInfo",
				"title":"展馆图片",
				"description":"",
				"exception":[]	
			},
			"expo_news":{
				"tag":"ExpoInfo",
				"title":"展会资讯",
				"description":"",
				"exception":[]	
			},
			"expo_tag":{
				"tag":"ExpoTag",
				"title":"展会标签",
				"description":"",
				"exception":["getlist"]	
			}
		},
		"home":{
			"home_siteinfo":{
				"tag":"HomeSiteInfo",
				"title":"本站信息",
				"description":"",
				"exception":[]	
			},
			"home_sitetag":{
				"tag":"HomeSiteInfo",
				"title":"本站信息标签",
				"description":"",
				"exception":[]	
			},
			"home_delete_img":{
				"tag":"HomeDeleteImg",
				"title":"临时图片操作",
				"description":"",
				"exception":[]	
			},
			"home_country_sort":{
				"tag":"Common",
				"title":"省份城市",
				"description":"",
				"exception":["getlist"]	
			},
			"home_friendlylinks":{
				"tag":"HomeFriendlyLinks",
				"title":"友情链接",
				"description":"",
				"exception":[]	
			},
			"home_illegal_keyword":{
				"tag":"HomeIllegalKeyword",
				"title":"违法关键字",
				"description":"",
				"exception":[]	
			},
			"home_user_prompt":{
				"tag":"HomeUserPrompt",
				"title":"用户中心提示",
				"description":"",
				"exception":[]	
			},
			"home_sys_message":{
				"tag":"HomeSysMessage",
				"title":"系统留言",
				"description":"",
				"exception":[]	
			},
			"home_admin_notice":{
				"tag":"HomeAdminNotice",
				"title":"管理员通知",
				"description":"",
				"exception":[]	
			},
			"home_message":{
				"tag":"HomeMessage",
				"title":"通用消息中心",
				"description":"",
				"exception":[]	
			},
			"home_mail_spread_set":{
				"tag":"HomeMail",
				"title":"推广邮件设置",
				"description":"",
				"exception":[]	
			},
			"home_email_template":{
				"tag":"HomeMail",
				"title":"邮件模板",
				"description":"",
				"exception":[]	
			},
			"home_res_picture":{
				"tag":"HomeResPicture",
				"title":"资源图片",
				"description":"",
				"exception":[]	
			},
			"home_async_email":{
				"tag":"HomeAsyncEmail",
				"title":"异步发送邮件",
				"description":"",
				"exception":[]	
			},
			"home_setting":{
				"tag":"HomeSetting",
				"title":"全局网站设置",
				"description":"",
				"exception":[]	
			},	
			"home_apply_del_info":{
				"tag":"HomeApplyDelInfo",
				"title":"维权及删除信息",
				"description":"",
				"exception":[]	
			}					
		},
		"help":{
			"help_info":{
				"tag":"HelpInfo",
				"title":"帮助中心信息",
				"description":"",
				"exception":[]	
			},		
			"help_tag":{
				"tag":"HelpInfo",
				"title":"帮助中心信息标签",
				"description":"",
				"exception":[]	
			},
			"help_func_error":{
				"tag":"HelpFuncError",
				"title":"用户功能报错",
				"description":"",
				"exception":[]	
			}			
		},
		"user":{
			"user_info":{
				"tag":"UserInfo",
				"title":"用户",
				"description":"",
				"exception":[]	
			},
			"user_group":{
				"tag":"UserInfo",
				"title":"用户组",
				"description":"",
				"exception":[]	
			},	
			"user_setting":{
				"tag":"UserGroup",
				"title":"会员设置",
				"description":"",
				"exception":[]	
			},	
			"user_trade_logs":{
				"tag":"UserTradeLogs",
				"title":"账号交易日志",
				"description":"",
				"exception":[]	
			},	
			"user_attestation_check":{
				"tag":"UserAttestationCheck",
				"title":"用户认证帐号密码",
				"description":"",
				"exception":[]	
			},	
			"user_apply_merge":{
				"tag":"UserApplyMerge",
				"title":"申请合并会员账号",
				"description":"",
				"exception":[]	
			},	
			"user_admin":{
				"tag":"UserAdmin",
				"title":"管理员操作",
				"description":"",
				"exception":[]	
			},	
			"user_admin_role":{
				"tag":"UserAdmin",
				"title":"管理员角色",
				"description":"",
				"exception":[]	
			},	
			"user_admin_log":{
				"tag":"UserAdmin",
				"title":"后台操作日志",
				"description":"",
				"exception":[]	
			},	
			"user_corp_file":{
				"tag":"UserCorpFile",
				"title":"公司档案",
				"description":"",
				"exception":[]	
			},	
			"user_corp_file_check":{
				"tag":"UserCorpFile",
				"title":"公司档案审核",
				"description":"",
				"exception":[]	
			},	
		}
}


