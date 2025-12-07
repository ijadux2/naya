" Naya filetype detection file
" Language: Naya
" Maintainer: Naya Team

" Detect .naya files
autocmd BufNewFile,BufRead *.naya set filetype=naya

" Set comment string for Naya
autocmd FileType naya setlocal commentstring=//\ %s

" Set makeprg for Naya
autocmd FileType naya setlocal makeprg=python3\ ~/.local/share/naya/naya.py\ %:p\ %:p:r

" Set errorformat for Naya compiler
autocmd FileType naya setlocal errorformat=%EError:\ %m,%WWarning:\ %m,%CLine\ %l:\ %m

" Enable folding for functions, structs, etc.
autocmd FileType naya setlocal foldmethod=syntax
autocmd FileType naya setlocal foldlevelstart=99

" Define syntax folding
autocmd Syntax naya syn region nayaFuncFold start="func\>" end="^}" transparent fold
autocmd Syntax naya syn region nayaStructFold start="struct\>" end="^}" transparent fold
autocmd Syntax naya syn region nayaUnionFold start="union\>" end="^}" transparent fold
autocmd Syntax naya syn region nayaEnumFold start="enum\>" end="^}" transparent fold
autocmd Syntax naya syn region nayaMatchFold start="match\>" end="^}" transparent fold

" Highlight matching braces
autocmd FileType naya setlocal showmatch

" Set indentation settings
autocmd FileType naya setlocal tabstop=4 shiftwidth=4 expandtab
autocmd FileType naya setlocal smartindent
autocmd FileType naya setlocal cindent
autocmd FileType naya setlocal cinoptions=:0,l1,t0,g0,(0

" Define indentation patterns
autocmd FileType naya setlocal indentkeys=0{,0},0),0],!^F,o,O,e
autocmd FileType naya setlocal indentexpr=GetNayaIndent()

function! GetNayaIndent()
  let line = getline(v:lnum)
  let prev_line = getline(v:lnum - 1)
  
  " Default to previous line's indent
  let indent = indent(v:lnum - 1)
  
  " Increase indent after opening brace
  if prev_line =~ '{\s*$'
    let indent += &shiftwidth
  endif
  
  " Decrease indent for closing brace
  if line =~ '^\s*}'
    let indent -= &shiftwidth
  endif
  
  " Increase indent after function declaration
  if prev_line =~ 'func.*{$'
    let indent += &shiftwidth
  endif
  
  " Increase indent after struct/union/enum declaration
  if prev_line =~ '\(struct\|union\|enum\).*$'
    let indent += &shiftwidth
  endif
  
  " Increase indent after if/while/for/match
  if prev_line =~ '\(if\|while\|for\|match\).*$'
    let indent += &shiftwidth
  endif
  
  " Decrease indent for else/catch
  if line =~ '^\s*\(else\|catch\)'
    let indent -= &shiftwidth
  endif
  
  return indent
endfunction

" Define text objects for Naya
autocmd FileType naya xnoremap <buffer> if :<C-U>call NayaTextObject('func')<CR>
autocmd FileType naya xnoremap <buffer> is :<C-U>call NayaTextObject('struct')<CR>
autocmd FileType naya xnoremap <buffer> iu :<C-U>call NayaTextObject('union')<CR>
autocmd FileType naya xnoremap <buffer> ie :<C-U>call NayaTextObject('enum')<CR>

function! NayaTextObject(type)
  let start_line = search('^\s*\<' . a:type . '\>', 'bnW')
  let end_line = search('^\s*}', 'nW')
  
  if start_line > 0 && end_line > 0
    execute start_line . ',' . end_line . 'normal! V'
  endif
endfunction

" Define compile commands
autocmd FileType naya nnoremap <buffer> <F5> :w<CR>:!python3 ~/.local/share/naya/naya.py %:p %:p:r<CR>
autocmd FileType naya nnoremap <buffer> <F6> :w<CR>:!python3 ~/.local/share/naya/naya.py %:p %:p:r && ./%:p:r<CR>
autocmd FileType naya nnoremap <buffer> <F7> :w<CR>:!cd %:p:h && ./build.sh<CR>

" Define LSP configuration
if exists(':LspStart')
  autocmd FileType naya LspStart python3 ~/.local/share/naya/lsp_server.py
endif

" Define completion
autocmd FileType naya setlocal completefunc=CompleteNaya

function! CompleteNaya(findstart, base)
  if a:findstart
    " Return the starting column
    let line = getline('.')
    let start = col('.') - 1
    while start > 0 && line[start - 1] =~ '\w'
      let start -= 1
    endwhile
    return start
  else
    " Return completion matches
    let matches = []
    
    " Keywords
    let keywords = ['func', 'if', 'else', 'while', 'for', 'return', 'import', 'export', 'extern', 'defer', 'try', 'catch', 'match', 'struct', 'union', 'enum', 'type', 'comptime', 'const', 'var', 'break', 'continue']
    for keyword in keywords
      if keyword =~ '^' . a:base
        call add(matches, {'word': keyword, 'kind': 'keyword'})
      endif
    endfor
    
    " Types
    let types = ['int', 'uint', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'string', 'bool', 'void', 'ptr', 'uptr', 'cptr']
    for type in types
      if type =~ '^' . a:base
        call add(matches, {'word': type, 'kind': 'type'})
      endif
    endfor
    
    " Constants
    let constants = ['true', 'false', 'null']
    for constant in constants
      if constant =~ '^' . a:base
        call add(matches, {'word': constant, 'kind': 'constant'})
      endif
    endfor
    
    " System calls
    if a:base =~ '^syscall\.'
      let syscalls = ['write', 'read', 'exit', 'open', 'close', 'mmap', 'munmap', 'fork', 'execve', 'waitpid', 'kill', 'pipe', 'dup', 'dup2']
      for syscall in syscalls
        if 'syscall.' . syscall =~ '^' . a:base
          call add(matches, {'word': 'syscall.' . syscall, 'kind': 'function'})
        endif
      endfor
    endif
    
    return matches
  endif
endfunction

" Define statusline
autocmd FileType naya setlocal statusline=%f\ %h%m%r%=%{NayaStatusLine()}

function! NayaStatusLine()
  let line = line('.')
  let col = col('.')
  let total_lines = line('$')
  return 'Naya [' . line . '/' . total_lines . ':' . col . ']'
endfunction

" Define quickfix commands
autocmd FileType naya command! -nargs=0 NayaCompile call NayaCompile()
autocmd FileType naya command! -nargs=0 NayaRun call NayaRun()
autocmd FileType naya command! -nargs=0 NayaBuild call NayaBuild()

function! NayaCompile()
  let output_file = expand('%:r')
  let cmd = 'python3 ~/.local/share/naya/naya.py ' . expand('%:p') . ' ' . output_file
  let result = system(cmd)
  
  if v:shell_error == 0
    echo 'Compilation successful: ' . output_file
  else
    echo 'Compilation failed: ' . result
  endif
endfunction

function! NayaRun()
  let output_file = expand('%:r')
  if !filereadable(output_file)
    call NayaCompile()
  endif
  
  if filereadable(output_file)
    let result = system('./' . output_file)
    echo 'Output: ' . result
  else
    echo 'Cannot run: executable not found'
  endif
endfunction

function! NayaBuild()
  let cmd = 'cd ' . expand('%:p:h') . ' && ./build.sh'
  let result = system(cmd)
  
  if v:shell_error == 0
    echo 'Build successful'
  else
    echo 'Build failed: ' . result
  endif
endfunction