## Empty list -- just use the empty environment for this.
nil <- function() {
  emptyenv()
}

## Test if a list is the empty list:
is_empty <- function(lis) {
  identical(lis, nil())
}

## Lisp-style linked list with 'car' and 'cdr' addresses, built around
## an environment (giving reference semantics).  Using an S3 class
## here purely for printing purposes later.
cons <- function(a, b) {
  e <- new.env(parent=nil())
  e$car <- a
  e$cdr <- b
  class(e) <- "linkedlist"
  e
}

## The standard 'car' and 'cdr' addressing functions:
car <- function(lis) {
  lis$car
}
cdr <- function(lis) {
  lis$cdr
}

## The usual convenience functions can be built around these:
cadr <- function(lis) {
  car(cdr(lis))
}

## Support for setting car/cdr is straightforward:
setcar <- function(lis, v) {
  lis$car <- v
}
setcdr <- function(lis, v) {
  lis$cdr <- v
}

## More R-ish
`car<-` <- function(lis, value) {
  setcar(lis, value)
  lis
}
`cdr<-` <- function(lis, value) {
  setcdr(lis, value)
  lis
}

## Convenience function for building list.  So where you'd write
##    '(1 2 3 4)
## with this function we'd write:
##    linkedlist(1, 2, 3, 4)
linkedlist <- function(el, ...) {
  if (missing(el)) {
    nil()
  } else {
    cons(el, linkedlist(...))
  }
}

## A print method.  Recursive, rather than stack based (and R's stack
## is not that big) and won't create beautiful output with large input
## or with non-atomic list elements.
print.linkedlist <- function(x, ...) {
  cat(sprintf("[linked list]:\n  %s\n", as.character(x)))
}
## Actual workhorse done via as.character()
as.character.linkedlist <- function(x) {
  head_str <- as.character(car(x))
  tail <- cdr(x)
  if (is_empty(tail)) {
    head_str
  } else {
    sprintf("(%s %s)", head_str, as.character(tail))
  }
}

## The above should give enough primitive support to implement usual
## functions that operate on linked lists:
insert_at <- function(new, k, lis) {
  if (is_empty(lis)) {
    linkedlist(new)
  } else if (k == 0) {
    cons(new, lis)
  } else {
    cons(car(lis),
         insert_at(new, k-1L, cdr(lis)))
  }
}

## Use:

## Construct a list of 1..4:
lis <- cons(1, cons(2, cons(3, cons(4, nil()))))
lis

car(lis)  # 1
cdr(lis)  # (2 (3 4))
cadr(lis) # 2

car(lis) <- -1
lis # (-1 (2 (3 4)))

## Copy the list:
lis2 <- lis
car(lis2) <- 1
lis2 # (1 (2 (3 4))) -- both the same due to shared environment
lis  # (1 (2 (3 4)))

## Insert element:
lis3 <- insert_at(10, 2L, lis)
lis3 # (1 (2 (10 (3 4))))
lis  # (1 (2 (3 4))) -- unchanged...