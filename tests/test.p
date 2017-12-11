forward foo(a, b);
native bar(a, b, c);
native blah(a, b, c, d);

main()
{
    bar(1, 2, 3);
    blah(4, 5, 6, 7);
    return 1;
}

public foo(a, b)
{
    return a - b;
}