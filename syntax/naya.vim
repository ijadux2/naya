" Vim syntax file for Naya programming language
" Language: Naya
" Maintainer: Naya Team
" Latest Revision: 2024

if exists("b:current_syntax")
  finish
endif

let s:keepcpo = &cpo
set cpo&vim

" Keywords
syn keyword nayaKeyword func if else while for return import export extern
syn keyword nayaKeyword defer try catch match struct union enum type
syn keyword nayaKeyword comptime const var break continue
syn keyword nayaConditional if else match
syn keyword nayaRepeat while for
syn keyword nayaStatement return break continue defer try catch
syn keyword nayaLabel case default

" Types
syn keyword nayaType int uint uint8 uint16 uint32 uint64
syn keyword nayaType int8 int16 int32 int64 float32 float64
syn keyword nayaType string bool void
syn keyword nayaType ptr uptr cptr
syn keyword nayaType Result Ok Err Arena Allocator

" Constants
syn keyword nayaConstant true false null

" Operators
syn match nayaOperator "\v\.\."
syn match nayaOperator "\v\=\="
syn match nayaOperator "\v\!\="
syn match nayaOperator "\v\<\="
syn match nayaOperator "\v\>\="
syn match nayaOperator "\v\-\>"
syn match nayaOperator "\v\=\>"
syn match nayaOperator "\v[\+\-\*/\%\=\>\<\!\&\|\^\~]"

" Delimiters
syn match nayaDelimiter "\v[\[\]\(\)\{\},\.]"

" Numbers
syn match nayaNumber "\v\<\d+\>"
syn match nayaNumber "\v\<\d+\.\d+\>"
syn match nayaNumber "\v\<0x[0-9a-fA-F]+\>"
syn match nayaNumber "\v\<0b[01]+\>"
syn match nayaNumber "\v\<0o[0-7]+\>"

" Strings
syn region nayaString start=/"/ skip=/\\\\\|\\"/ end=/"/
syn region nayaChar start=/'/ skip=/\\\\\|\\'/ end=/'/

" Comments
syn keyword nayaTodo TODO FIXME XXX NOTE contained
syn match nayaComment "//.*" contains=nayaTodo
syn region nayaComment start="/\*" end="\*/" contains=nayaTodo

" Function definitions
syn match nayaFunction "\v<func>\s+\zs\w+\ze\s*\("

" Struct/Union/Enum names
syn match nayaStructure "\v<(struct|union|enum)>\s+\zs\w+\ze"
syn match nayaStructure "\vtype>\s+\zs\w+\ze\s*\="

" Type annotations
syn match nayaTypeDecl "\v\w+\s*\zs:\ze\s*\w+"

" System calls
syn match nayaSyscall "\vsyscall\.\w+"

" Generic parameters
syn match nayaGeneric "\v\w+\s*\zs:\ze\s*type\>"

" Comptime expressions
syn match nayaComptime "\vcomptime\s+\w+"

" Error handling
syn match nayaError "\v(try|catch|Result|Ok|Err)"

" Memory management
syn match nayaMemory "\v(alloc|free|malloc|Arena|Allocator)"

" Import statements
syn match nayaImport "\vimport>\s+\zs\w+\ze"

" Export statements
syn match nayaExport "\vexport>\s*\zs\"[^\"]*\"\ze"

" Extern blocks
syn match nayaExtern "\vextern>\s*\zs\"[^\"]*\"\ze"

" Field access
syn match nayaFieldAccess "\v\.\zs\w+\ze"

" Method calls
syn match nayaMethodCall "\v\.\zs\w+\ze\s*\("

" Array access
syn match nayaArrayAccess "\v\w+\s*\zs\[\ze"

" Define the default highlighting
hi def link nayaKeyword Keyword
hi def link nayaConditional Conditional
hi def link nayaRepeat Repeat
hi def link nayaStatement Statement
hi def link nayaLabel Label
hi def link nayaType Type
hi def link nayaTypedef Typedef
hi def link nayaStructure Structure
hi def link nayaFunction Function
hi def link nayaConstant Constant
hi def link nayaNumber Number
hi def link nayaString String
hi def link nayaChar Character
hi def link nayaComment Comment
hi def link nayaTodo Todo
hi def link nayaOperator Operator
hi def link nayaDelimiter Delimiter
hi def link nayaSyscall Function
hi def link nayaGeneric Special
hi def link nayaComptime Special
hi def link nayaError Error
hi def link nayaMemory Special
hi def link nayaImport Include
hi def link nayaExport Special
hi def link nayaExtern Special
hi def link nayaFieldAccess Identifier
hi def link nayaMethodCall Function
hi def link nayaArrayAccess Identifier
hi def link nayaTypeDecl Type

" Set syntax
let b:current_syntax = "naya"

let &cpo = s:keepcpo
unlet s:keepcpo