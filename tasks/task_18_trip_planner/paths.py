import heapq


def shortest(roads, source):
    dist = {source: 0}
    prev = {}
    heap = [(0, source)]
    done = set()
    while heap:
        d, city = heapq.heappop(heap)
        if city in done:
            continue
        done.add(city)
        for nxt, km in roads.neighbours(city):
            nd = d + km
            if nd < dist.get(nxt, nd + 1):
                dist[nxt] = nd
                prev[nxt] = city
                heapq.heappush(heap, (nd, nxt))
    return dist, prev
