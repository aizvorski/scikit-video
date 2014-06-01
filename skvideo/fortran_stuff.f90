subroutine foo(x)
    integer, dimension(4), intent(out) :: x
    x(1) = 4
    x(2) = 3
    x(3) = 2
    x(4) = 1
end subroutine
