# Changes

## 1.4

* Relaxed the dependencies needed for pymountebank and also used tenacity as retrying is deprecated.

## 1.3

* Allows status codes to be used to be able to mock non-200 responses.

## 1.2

* `repeat` argument added to `Imposter.add_stub`
* Multiple responses can be added to the same stub

## 1.1

* Imposter.mockhttp by default waits for mountebank to become accessible

## 1.0

* mountebank pip was born
