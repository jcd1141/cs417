Part 1:

Solutions:

    Solution A: Solution A first check if K is less than or equal to 0. If it is, it returns []. Afterwards, it makes a counter to count everything once. Then it makes tuples like (count, -index, item) so "ties" go to whoever showed up first. It uses heapq.nlargest to grab the top k without sorting everything. Then it converts it back to (item, count).

    Solution B: Solution B stars the same as A, checking if k <= 0, then creating a counter. The it builds a list, where index keeps track of appearence order. After that it sorts the entire list using (-count, index), so bigger counts come first and ties go to earlier items. Finally it just slices the first k results.

    Solution C: Starts by checking if k <= 0, but then becomes much more complicated. It goes through the whole list using a set and list to find appearence order. Then for each item it calls items.count(item), which means it scans the entire list again every time. It builds (item, count) pairs and then sorts by count. Since Python sort is stable, ties stay in the same order from before. 

Predictions:

    1: C breaks first. It keeps rescanning the list over and over with count(), so it’s gonna get slow fast when the input gets bigger.

    2: I’d trust B at 3am. It’s the easiest to read and understand quickly, and everything it’s doing is very straightforward. You can clearly see it counts once, builds a list, then sorts with a simple rule, so it’s easy to verify that ties and ordering are correct. If something was wrong, it would be easier to debug compared to A, which uses a heap and tuple tricks that take a bit more thinking to follow, and C is much more complicated.



