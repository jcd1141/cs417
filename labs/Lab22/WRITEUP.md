Part 1:

Solutions:

    Solution A: Solution A first check if K is less than or equal to 0. If it is, it returns []. Afterwards, it makes a counter to count everything once. Then it makes tuples like (count, -index, item) so "ties" go to whoever showed up first. It uses heapq.nlargest to grab the top k without sorting everything. Then it converts it back to (item, count).

    Solution B: Solution B stars the same as A, checking if k <= 0, then creating a counter. The it builds a list, where index keeps track of appearence order. After that it sorts the entire list using (-count, index), so bigger counts come first and ties go to earlier items. Finally it just slices the first k results.

    Solution C: Starts by checking if k <= 0, but then becomes much more complicated. It goes through the whole list using a set and list to find appearence order. Then for each item it calls items.count(item), which means it scans the entire list again every time. It builds (item, count) pairs and then sorts by count. Since Python sort is stable, ties stay in the same order from before. 

Predictions:

    1: C breaks first. It keeps rescanning the list over and over with count(), so it’s gonna get slow fast when the input gets bigger.

    2: I’d trust B at 3am. It’s the easiest to read and understand quickly, and everything it’s doing is very straightforward. You can clearly see it counts once, builds a list, then sorts with a simple rule, so it’s easy to verify that ties and ordering are correct. If something was wrong, it would be easier to debug compared to A, which uses a heap and tuple tricks that take a bit more thinking to follow, and C is much more complicated.

Part 2:

Best: A is the best because it only counts everything once with Counter, then uses heapq.nlargest instead of sorting everything. That means it only really focuses on the top k instead of doing extra work. The tuple (count, -i, item) handles ties correctly since earlier items win. It’s a little harder to read at first because of the tuple and negative index, but overall it’s the most efficient one.

Mid: B is still good, just not as efficient. It also uses Counter, but then it builds a list of all items and sorts the entire thing with entries.sort(...). That means even if k is small, it still sorts everything which is extra work. The good part is it’s really easy to read and understand since the sort key (-count, i) is very clear. It's not as optimized as A.

Worst: C is the worst one. It loops through the list, then for every item it calls items.count(item), which means it keeps scanning the whole list over and over. That’s slower with bigger inputs. It works, but it’s inefficient and not as clean as the other two.

Part 3:

=== Regime 1 — small fixed vocabulary (50 distinct items) ===
         n |   unique |     A (heap) |     B (sort) |     C (loop)
------------------------------------------------------------------------
       100 |       50 |       0.07ms |       0.05ms |       0.11ms
     1,000 |       50 |       0.09ms |       0.06ms |       0.74ms
    10,000 |       50 |       1.06ms |       0.47ms |       7.37ms
   100,000 |       50 |       6.60ms |       5.22ms |      71.41ms

=== Regime 2 — vocabulary scales with n (unique ≈ n/2) ===
         n |   unique |     A (heap) |     B (sort) |     C (loop)
------------------------------------------------------------------------
       100 |       50 |       0.06ms |       0.02ms |       0.07ms
     1,000 |      500 |       0.26ms |       0.21ms |       7.39ms
    10,000 |    5,000 |       2.12ms |       3.50ms |     751.32ms

    mypy --strict src/solution_a.py src/solution_b.py src/solution_c.py
    src/solution_c.py:29: error: Incompatible return value type (got "list[tuple[str, int]]", expected "list[int]")  [return-value]
    Found 1 error in 1 file (checked 3 source files)

    Paragraph: The benchmark mostly confirmed my ranking, but it also showed some differences. In Regime 1, B was actually a little faster than A at every size, which makes sense since the number of unique items is small so sorting isn’t that expensive. But in Regime 2, A becomes better as things scale (at 10,000 A is 2.12ms while B is 3.50ms), so A handles larger and more complex inputs better. C was by far the worst in both, especially in Regime 2 where it jumps to 751.32ms, which shows how bad the repeated count() calls are. mypy said said the return type was wrong for Solution C, expecting list[int] but getting list[tuple[str, int]], so the type hint is incorrect. The difference between the two regimes shows that B is fine when the number of unique items is small, but A is better when the data grows, and C really doesn’t fit either case.

Part 4:
   
    A: Yes, my ranking changes a little. If the input is always under 50 items and it only runs once a week, I would probably put B over A. B is easier to read and understand right away, and in a small workload the extra sorting really does not matter much. The benchmark also showed B was a little faster in Regime 1, so in this case I think B makes the most sense. C is still last because it still does repeated work and still has the wrong type hint.


    B: Here my ranking stays A, then B, then C. If this runs 10,000 times per second and the workload looks like Regime 2, performance matters a lot more, and A clearly handled that better than B in the benchmark. B is still readable, but sorting everything every time becomes a bigger problem when the number of unique items grows. C becomes even worse here because the repeated count() calls would be way too slow, and the bad type hint is another thing you would not want in an important code path. In this case the extra efficiency in A matters more than the extra simplicity in B.

Part 5:

    The solution I would reject would be C. While it works, it is by far the most inneficient and least optimized of the group. For every unique item, it scans the list again. This makes the time complexity around O(n^2) in worse cases, especially when there are a lot of distinct items. In comparison, A and B both use Counter which is closer to O(n) for counting, so they scale much better. There is also a type hint problem since the function says it returns list[int], but it actually returns tuples. The mypy caught this. I would suggest replacing the repeated count() calls with Counter(items) and fixing the return type to list[tuple[str, int]]. That would keep the same behavior while making it much faster and cleaner.