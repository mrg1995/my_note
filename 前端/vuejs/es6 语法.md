## es6 语法

### let 和 const 命令

#### 1 .let

- 声明的变量只在 let所在的代码块有效
  - `for`循环有个特别之处，设置循环变量的那部分是一个父作用域，而循环体内部是一个单独的子作用域。
- 不存在变量提升  (let声明的变量,不能在声明前使用)
- 暂时性死区
  - ES6 明确规定，如果区块中存在`let`和`const`命令，这个区块对这些命令声明的变量，从一开始就形成了封闭作用域。凡是在声明之前就使用这些变量，就会报错。(官话)
    - 存在全局变量`tmp`，但是块级作用域内`let`又声明了一个局部变量`tmp`，导致后者绑定这个块级作用域，所以这个块级作用域里,在`let`声明变量前，对`tmp`赋值会报错。(人话)
- 不允许在相同作用域重复声明**同一个变量**

#### 2. 块级作用域

- 示例

  ```javascript
  function f1() {
    let n = 5;
    if (true) {
      let n = 10; //块级作用域  对 外面的函数作用域无影响 
    }
    console.log(n); // 5
  }
  ```

  - 内层作用域可以定义外层作用域的同名变量
  - 外层作用域无法读取内部作用域的变量

- 在块级作用域中应该尽量避免定义函数,如果确实要定义,应该写成函数表达式

  ```javascript
  // 函数表达式
  {
    let a = 'secret';
    let f = function () {
      return a;
    };
  }
  ```

#### 3. const命令

- 声明的是一个只读的常量,一旦声明,常量的值就不能改变
- const一旦声明变量,就必须立即初始化,不能留到后面复制
- 作用域与let相同,只在声明的块级作用域中有效
- const声明的常量也是不可提升,不可重复声明的

#### 4.顶层对象的属性

- 浏览器环境指的是window对象,node指的是global对象

- var命令和function命令声明的全局变量依旧是顶层对象的属性

- let,const,class声明的全局变量不属于顶层对象的属性

- ```javascript
  //示例
  var a = 1;
  // 如果在 Node 的 REPL 环境，可以写成 global.a
  // 或者采用通用方法，写成 this.a
  window.a // 1

  let b = 1;
  window.b // undefined
  ```

#### 5.global对象



## 变量的解构赋值

#### 1. 数组的解构赋值

- 可以从数据中提取值,按照对应位置,对变量赋值

  - let [a, b, c] = [1, 2, 3];
  - 如果解构不成功,变量的值等于undefined

- 解构赋值允许指定默认值

  - ```javascript
    // 只有当数组成员是undefined时,默认值才会生效
    let [x = 1] = [undefined];
    x // 1

    let [x = 1] = [null];
    x // null
    ```

#### 2. 对象的解构赋值

- 对象的解构赋值内部机制，是先找到同名属性，然后再赋给对应的变量。真正被赋值的是后者，而不是前者。

  - let { foo: foo, bar: bar } = { foo: "aaa", bar: "bbb" };

  - ```javascript
    let { foo: baz } = { foo: "aaa", bar: "bbb" };
    baz // "aaa"
    foo // error: foo is not defined
    //foo 是匹配的模式   baz才是被赋值的变量
    ```

- 如果解构失败,变量的值等于undefined

#### 3. 字符串的解构赋值

- 字符串也可以解构赋值

  - ```
    //字符串被转化为类似数组的对象
    const [a, b, c, d, e] = 'hello';
    ```

  - ```
    //类似数组的对象都有length属性 ,因此还可以对这个属性解构赋值
    let {length : len} = 'hello';
    len // 5
    ```

#### 4. 数值和布尔值的解构赋值

#### 5. 函数参数的解构赋值

- 函数参数也可以解构赋值

  - ```javascript
    function add([x, y]){
      return x + y;
    }
    add([1, 2]); // 3
    ```

- 函数参数的解构也可以使用默认值

  - ```
    function move({x = 0, y = 0} = {}) {
      return [x, y];
    }

    move({x: 3, y: 8}); // [3, 8]
    move({x: 3}); // [3, 0]
    move({}); // [0, 0]
    move(); // [0, 0]
    ```

#### 6. 圆括号问题

- 赋值的非模式部分,可以使用圆括号

#### 7 . 用途

- 交换变量的值

- 从函数返回多个值

- 函数参数的定义

- 提取json数据

- 函数参数的默认值

- 遍历map解构

  - ```JavaScript
    const map = new Map();
    map.set('first', 'hello');
    map.set('second', 'world');

    for (let [key, value] of map) {
      console.log(key + " is " + value);
    }
    // first is hello
    // second is world
    // 获取键名
    for (let [key] of map) {
      // ...
    }

    // 获取键值
    for (let [,value] of map) {
      // ...
    }
    ```

## 字符串的扩展

- 字符的uniode表示法

  - ```javascript
    //JavaScript 共有 6 种方法可以表示一个字符。
    '\z' === 'z'  // true
    '\172' === 'z' // true
    '\x7A' === 'z' // true
    '\u007A' === 'z' // true
    '\u{7A}' === 'z' // true
    ```

- 字符串的遍历器接口

  - ```
    for (let codePoint of 'foo') {
      console.log(codePoint)
    }
    // "f"
    // "o"
    // "o"
    ```

- includes(),startsWith(),endsWith()

  - **includes()**：返回布尔值，表示是否找到了参数字符串。
  - **startsWith()**：返回布尔值，表示参数字符串是否在原字符串的头部。
  - **endsWith()**：返回布尔值，表示参数字符串是否在原字符串的尾部。

- padStart(),padEnd()

  ```
  '1'.padStart(10, '0') // "0000000001"
  '12'.padStart(10, '0') // "0000000012"
  '123456'.padStart(10, '0') // "0000123456"
  ```

## 函数的扩展

- 函数参数的默认值

  - ```
    function Point(x = 0, y = 0) {
      this.x = x;
      this.y = y;
    }

    const p = new Point();
    p // { x: 0, y: 0 }
    ```

  ​

- rest参数

  - 形式为`...变量名`

  - ```
    function add(...values) {
      let sum = 0;

      for (var val of values) {
        sum += val;
      }

      return sum;
    }

    add(2, 5, 3) // 10
    ```

- 箭头函数

  - ```
    var f = v => v;

    // 等同于
    var f = function (v) {
      return v;
    };
    ```

  - ```
    var f = () => 5;
    // 等同于
    var f = function () { return 5 };

    var sum = (num1, num2) => num1 + num2;
    // 等同于
    var sum = function(num1, num2) {
      return num1 + num2;
    };
    ```

  - ```
    var sum = (num1, num2) => { return num1 + num2; }
    ```

  - 简化回调函数

    - // 正常函数写法
      var result = values.sort(function (a, b) {
        return a - b;
      });

      // 箭头函数写法
      var result = values.sort((a, b) => a - b);



## set 和 map数据结构

#### set

- 类似于python的set  

  ```
  const s = new Set();

  [2, 3, 5, 4, 5, 2, 2].forEach(x => s.add(x));

  for (let i of s) {
    console.log(i);
  }
  // 2 3 5 4
  ```

- set实例的属性和方法

  - Set 结构的实例有以下属性。
    - `Set.prototype.constructor`：构造函数，默认就是`Set`函数。
    - `Set.prototype.size`：返回`Set`实例的成员总数。
  - Set 实例的方法分为两大类：操作方法（用于操作数据）和遍历方法（用于遍历成员）。下面先介绍四个操作方法。
    - `add(value)`：添加某个值，返回 Set 结构本身。
    - `delete(value)`：删除某个值，返回一个布尔值，表示删除是否成功。
    - `has(value)`：返回一个布尔值，表示该值是否为`Set`的成员。
    - `clear()`：清除所有成员，没有返回值。

- 遍历操作

#### map

- 类似于python的dict,但是map可以把对象作为键(不仅仅是字符串)

- map.set(),map.get()

- 实例的属性和操作方法

  **（1）size 属性**

  `size`属性返回 Map 结构的成员总数。

  ```
  const map = new Map();
  map.set('foo', true);
  map.set('bar', false);

  map.size // 2
  ```

  **（2）set(key, value)**

  `set`方法设置键名`key`对应的键值为`value`，然后返回整个 Map 结构。如果`key`已经有值，则键值会被更新，否则就新生成该键。

  ```
  const m = new Map();

  m.set('edition', 6)        // 键是字符串
  m.set(262, 'standard')     // 键是数值
  m.set(undefined, 'nah')    // 键是 undefined
  ```

  `set`方法返回的是当前的`Map`对象，因此可以采用链式写法。

  ```
  let map = new Map()
    .set(1, 'a')
    .set(2, 'b')
    .set(3, 'c');
  ```

  **（3）get(key)**

  `get`方法读取`key`对应的键值，如果找不到`key`，返回`undefined`。

  ```
  const m = new Map();

  const hello = function() {console.log('hello');};
  m.set(hello, 'Hello ES6!') // 键是函数

  m.get(hello)  // Hello ES6!
  ```

  **（4）has(key)**

  `has`方法返回一个布尔值，表示某个键是否在当前 Map 对象之中。

  ```
  const m = new Map();

  m.set('edition', 6);
  m.set(262, 'standard');
  m.set(undefined, 'nah');

  m.has('edition')     // true
  m.has('years')       // false
  m.has(262)           // true
  m.has(undefined)     // true
  ```

  **（5）delete(key)**

  `delete`方法删除某个键，返回`true`。如果删除失败，返回`false`。

  ```
  const m = new Map();
  m.set(undefined, 'nah');
  m.has(undefined)     // true

  m.delete(undefined)
  m.has(undefined)       // false
  ```

  **（6）clear()**

  `clear`方法清除所有成员，没有返回值。

  ```
  let map = new Map();
  map.set('foo', true);
  map.set('bar', false);

  map.size // 2
  map.clear()
  map.size // 0
  ```

- 遍历方法

  - `keys()`：返回键名的遍历器。
  - `values()`：返回键值的遍历器。
  - `entries()`：返回所有成员的遍历器。
  - `forEach()`：遍历 Map 的所有成员。

- 与其他数据结构的相互转换

  **（1）Map 转为数组**

  前面已经提过，Map 转为数组最方便的方法，就是使用扩展运算符（`...`）。

  ```
  const myMap = new Map()
    .set(true, 7)
    .set({foo: 3}, ['abc']);
  [...myMap]
  // [ [ true, 7 ], [ { foo: 3 }, [ 'abc' ] ] ]
  ```

  **（2）数组 转为 Map**

  将数组传入 Map 构造函数，就可以转为 Map。

  ```
  new Map([
    [true, 7],
    [{foo: 3}, ['abc']]
  ])
  // Map {
  //   true => 7,
  //   Object {foo: 3} => ['abc']
  // }
  ```

  **（3）Map 转为对象**

  如果所有 Map 的键都是字符串，它可以无损地转为对象。

  ```
  function strMapToObj(strMap) {
    let obj = Object.create(null);
    for (let [k,v] of strMap) {
      obj[k] = v;
    }
    return obj;
  }

  const myMap = new Map()
    .set('yes', true)
    .set('no', false);
  strMapToObj(myMap)
  // { yes: true, no: false }
  ```

  如果有非字符串的键名，那么这个键名会被转成字符串，再作为对象的键名。

  **（4）对象转为 Map**

  ```
  function objToStrMap(obj) {
    let strMap = new Map();
    for (let k of Object.keys(obj)) {
      strMap.set(k, obj[k]);
    }
    return strMap;
  }

  objToStrMap({yes: true, no: false})
  // Map {"yes" => true, "no" => false}
  ```

  **（5）Map 转为 JSON**

  Map 转为 JSON 要区分两种情况。一种情况是，Map 的键名都是字符串，这时可以选择转为对象 JSON。

  ```
  function strMapToJson(strMap) {
    return JSON.stringify(strMapToObj(strMap));
  }

  let myMap = new Map().set('yes', true).set('no', false);
  strMapToJson(myMap)
  // '{"yes":true,"no":false}'
  ```

  另一种情况是，Map 的键名有非字符串，这时可以选择转为数组 JSON。

  ```
  function mapToArrayJson(map) {
    return JSON.stringify([...map]);
  }

  let myMap = new Map().set(true, 7).set({foo: 3}, ['abc']);
  mapToArrayJson(myMap)
  // '[[true,7],[{"foo":3},["abc"]]]'
  ```

  **（6）JSON 转为 Map**

  JSON 转为 Map，正常情况下，所有键名都是字符串。

  ```
  function jsonToStrMap(jsonStr) {
    return objToStrMap(JSON.parse(jsonStr));
  }

  jsonToStrMap('{"yes": true, "no": false}')
  // Map {'yes' => true, 'no' => false}
  ```

## Promise

- ```
  //Promise构造函数接受一个函数作为参数，该函数的两个参数分别是resolve和reject。
  const promise = new Promise(function(resolve, reject) {
    // ... some code

    if (/* 异步操作成功 */){
      resolve(value);
    } else {
      reject(error);
    }
  });
  ```

  ```
  //Promise实例生成以后，可以用then方法分别指定resolved状态和rejected状态的回调函数。
  promise.then(function(value) {
    // success
  }, function(error) {
    // failure
  });
  ```

- ```
  //异步加载图片的例子。
  function loadImageAsync(url) {
    return new Promise(function(resolve, reject) {
      const image = new Image();

      image.onload = function() {
        resolve(image);
      };

      image.onerror = function() {
        reject(new Error('Could not load image at ' + url));
      };

      image.src = url;
    });
  }
  ```

## class

- ```javascript
  //定义类
  class Point {
    constructor(x, y) {
      this.x = x;
      this.y = y;
    }

    toString() {
      return '(' + this.x + ', ' + this.y + ')';
    }
  }
  //里面有一个constructor方法，这就是构造方法，而this关键字则代表实例对象。
  ```

- ```
  //使用类新建实例
  class Bar {
    doStuff() {
      console.log('stuff');
    }
  }

  var b = new Bar();
  b.doStuff() // "stuff"
  ```

## Module的语法

- ```
  // ES6模块
  import { stat, exists, readFile } from './fs.js';
  ```

- export命令

  - 模块功能主要由两个命令构成：`export`和`import`。`export`命令用于规定模块的对外接口，`import`命令用于输入其他模块提供的功能。

  - 一个模块就是一个独立的文件。该文件内部的所有变量，外部无法获取。如果你希望外部能够读取模块内部的某个变量，就必须使用`export`关键字输出该变量

    - ```
      // 示例
      // profile.js
      export var firstName = 'Michael';
      export var lastName = 'Jackson';
      export var year = 1958;

      // profile.js
      var firstName = 'Michael';
      var lastName = 'Jackson';
      var year = 1958;

      export {firstName, lastName, year};

      //输出函数  使用as重命名
      function v1() { ... }
      function v2() { ... }

      export {
        v1 as streamV1,
        v2 as streamV2,
        v2 as streamLatestVersion
      };
      ```

- import命令

  - 类似于python的import

  - 在加载模块中不允许修改导入的接口,属性是可以修改的,但是尽量吧导入的都当做只读的

  - 加载写法

    - ```
      // 某些接口的加载
      import { area, circumference } from './circle';

      console.log('圆面积：' + area(4));
      console.log('圆周长：' + circumference(14));
      ```

    - ```
      //整体模块的加载
      import * as circle from './circle';

      console.log('圆面积：' + circle.area(4));
      console.log('圆周长：' + circle.circumference(14));
      ```

- export default 命令

  - 与普通的 输出输入 对比

    - ```
      // 第一组
      export default function crc32() { // 输出
        // ...
      }

      import crc32 from 'crc32'; // 输入

      // 第二组
      export function crc32() { // 输出
        // ...
      };

      import {crc32} from 'crc32'; // 输入
      ```

## 编程风格

- 字符串

  - 静态字符串一律使用单引号或反引号，不使用双引号。动态字符串使用反引号。

  - ```
    // bad
    const a = "foobar";
    const b = 'foo' + a + 'bar';

    // acceptable
    const c = `foobar`;

    // good
    const a = 'foobar';
    const b = `foo${a}bar`;
    ```

- 解构赋值

  使用数组成员对变量赋值时，优先使用解构赋值。

  ```
  const arr = [1, 2, 3, 4];

  // bad
  const first = arr[0];
  const second = arr[1];

  // good
  const [first, second] = arr;
  ```

  函数的参数如果是对象的成员，优先使用解构赋值。

  ```
  // bad
  function getFullName(user) {
    const firstName = user.firstName;
    const lastName = user.lastName;
  }

  // good
  function getFullName(obj) {
    const { firstName, lastName } = obj;
  }

  // best
  function getFullName({ firstName, lastName }) {
  	...
  }
  ```

  如果函数返回多个值，优先使用对象的解构赋值，而不是数组的解构赋值。这样便于以后添加返回值，以及更改返回值的顺序。

  ```
  // bad
  function processInput(input) {
    return [left, right, top, bottom];
  }

  // good
  function processInput(input) {
    return { left, right, top, bottom };
  }

  const { left, right } = processInput(input);
  ```

- 数组

  - 拷贝数组

    ```
    // bad
    const len = items.length;
    const itemsCopy = [];
    let i;

    for (i = 0; i < len; i++) {
      itemsCopy[i] = items[i];
    }

    // good
    const itemsCopy = [...items];
    ```

  - 使用 Array.from 方法，将类似数组的对象转为数组。

    ```
    const foo = document.querySelectorAll('.foo');
    const nodes = Array.from(foo);
    ```

- 函数

  立即执行函数可以写成箭头函数的形式。

  ```
  (() => {
    console.log('Welcome to the Internet.');
  })();
  ```

  那些需要使用函数表达式的场合，尽量用箭头函数代替。因为这样更简洁，而且绑定了 this。

  ```
  // bad
  [1, 2, 3].map(function (x) {
    return x * x;
  });

  // good
  [1, 2, 3].map((x) => {
    return x * x;
  });

  // best
  [1, 2, 3].map(x => x * x);
  ```

  箭头函数取代`Function.prototype.bind`，不应再用 self/_this/that 绑定 this。

  ```
  // bad
  const self = this;
  const boundMethod = function(...params) {
    return method.apply(self, params);
  }

  // acceptable
  const boundMethod = method.bind(this);

  // best
  const boundMethod = (...params) => method.apply(this, params);
  ```

  简单的、单行的、不会复用的函数，建议采用箭头函数。如果函数体较为复杂，行数较多，还是应该采用传统的函数写法。

  所有配置项都应该集中在一个对象，放在最后一个参数，布尔值不可以直接作为参数。

  ```
  // bad
  function divide(a, b, option = false ) {
  }

  // good
  function divide(a, b, { option = false } = {}) {
  }

  ```

  不要在函数体内使用 arguments 变量，使用 rest 运算符（...）代替。因为 rest 运算符显式表明你想要获取参数，而且 arguments 是一个类似数组的对象，而 rest 运算符可以提供一个真正的数组。

  ```
  // bad
  function concatenateAll() {
    const args = Array.prototype.slice.call(arguments);
    return args.join('');
  }

  // good
  function concatenateAll(...args) {
    return args.join('');
  }

  ```

  使用默认值语法设置函数参数的默认值。

  ```
  // bad
  function handleThings(opts) {
    opts = opts || {};
  }

  // good
  function handleThings(opts = {}) {
    // ...
  }
  ```

- map结构

  注意区分 Object 和 Map，只有模拟现实世界的实体对象时，才使用 Object。如果只是需要`key: value`的数据结构，使用 Map 结构。因为 Map 有内建的遍历机制。

  ```
  let map = new Map(arr);

  for (let key of map.keys()) {
    console.log(key);
  }

  for (let value of map.values()) {
    console.log(value);
  }

  for (let item of map.entries()) {
    console.log(item[0], item[1]);
  }
  ```

- Class

  总是用 Class，取代需要 prototype 的操作。因为 Class 的写法更简洁，更易于理解。

  ```
  // bad
  function Queue(contents = []) {
    this._queue = [...contents];
  }
  Queue.prototype.pop = function() {
    const value = this._queue[0];
    this._queue.splice(0, 1);
    return value;
  }

  // good
  class Queue {
    constructor(contents = []) {
      this._queue = [...contents];
    }
    pop() {
      const value = this._queue[0];
      this._queue.splice(0, 1);
      return value;
    }
  }
  ```

  使用`extends`实现继承，因为这样更简单，不会有破坏`instanceof`运算的危险。

  ```
  // bad
  const inherits = require('inherits');
  function PeekableQueue(contents) {
    Queue.apply(this, contents);
  }
  inherits(PeekableQueue, Queue);
  PeekableQueue.prototype.peek = function() {
    return this._queue[0];
  }

  // good
  class PeekableQueue extends Queue {
    peek() {
      return this._queue[0];
    }
  }
  ```

- 模块

  首先，Module 语法是 JavaScript 模块的标准写法，坚持使用这种写法。使用`import`取代`require`。

  ```
  // bad
  const moduleA = require('moduleA');
  const func1 = moduleA.func1;
  const func2 = moduleA.func2;

  // good
  import { func1, func2 } from 'moduleA';

  ```

  使用`export`取代`module.exports`。

  ```
  // commonJS的写法
  var React = require('react');

  var Breadcrumbs = React.createClass({
    render() {
      return <nav />;
    }
  });

  module.exports = Breadcrumbs;

  // ES6的写法
  import React from 'react';

  class Breadcrumbs extends React.Component {
    render() {
      return <nav />;
    }
  };

  export default Breadcrumbs;
  ```

  如果模块只有一个输出值，就使用`export default`，如果模块有多个输出值，就不使用`export default`，`export default`与普通的`export`不要同时使用。

  不要在模块输入中使用通配符。因为这样可以确保你的模块之中，有一个默认输出（export default）。

  ```
  // bad
  import * as myObject from './importModule';

  // good
  import myObject from './importModule';

  ```

  如果模块默认输出一个函数，函数名的首字母应该小写。

  ```
  function makeStyleGuide() {
  }

  export default makeStyleGuide;

  ```

  如果模块默认输出一个对象，对象名的首字母应该大写。

  ```
  const StyleGuide = {
    es6: {
    }
  };

  export default StyleGuide;
  ```