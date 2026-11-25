// Enumerate every unordered pair of rooted halves and flag possible joint collisions.
// Compile: c++ -std=c++17 -O3 verify_joint_range.cpp -o verify_joint_range
// Arguments: maximum half order, number of memory buckets, minimum half order,
// and optionally "log" to emit all candidate pairs for verify_short_witnesses.py.
// Example full run: ./verify_joint_range 14 20 1 log > candidates.txt
// Requires a C++17 compiler supporting unsigned 128-bit integers (Clang or GCC).
// Distinct modular evaluations certify distinct exact polynomials.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using Word = std::uint64_t;
constexpr Word prime = (Word(1) << 61) - 1;
constexpr Word x = 72819257, y = 89365429;
Word add(Word a, Word b) {
    Word r = a + b;
    return r >= prime ? r - prime : r;
}
Word mul(Word a, Word b) {
    __uint128_t p = __uint128_t(a) * b;
    return add(Word(p & prime), Word(p >> 61));
}

struct Rooted {
    int size;
    std::vector<int> children;
    Word rooted, whole, adjusted; // evaluated R, H, and H+(y-1)R
    std::vector<Word> cut; // A_B below weight |B|, U_B specialization at |B|
};
std::vector<Rooted> trees;
std::vector<Word> weight;

void emit(int size, const std::vector<int>& children) {
    Word rooted = x, whole = 0;
    std::vector<Word> a{1};
    for (int id : children) {
        const auto& c = trees[id];
        rooted = mul(rooted, add(y, c.rooted));
        whole = add(whole, c.adjusted);
        std::vector<Word> next(a.size() + c.size, 0);
        for (size_t i=0; i<a.size(); ++i)
            for (int j=0; j<=c.size; ++j)
                next[i+j] = add(next[i+j], mul(a[i], c.cut[j]));
        a.swap(next);
    }
    whole = add(whole, rooted);
    Word unrooted_cut = 0;
    for (int k=0; k<size; ++k)
        unrooted_cut = add(unrooted_cut, mul(a[k], weight[size-k]));
    a.push_back(unrooted_cut);
    trees.push_back({size, children, rooted, whole, add(whole, mul(y-1, rooted)), std::move(a)});
}

void generate(int size, int remaining, int lower, std::vector<int>& children) {
    if (!remaining) {
        emit(size, children);
        return;
    }
    // Children of size >= size are never reached, including newly emitted trees.
    for (int i=lower; i<int(trees.size()) && trees[i].size<=remaining; ++i) {
        children.push_back(i);
        generate(size, remaining-trees[i].size, i, children);
        children.pop_back();
    }
}

struct Pair {
    Word census;
    int left, right;
};

bool same_slice(const Pair& a, const Pair& b, int h) {
    auto coefficient = [](const Pair& p, int k) {
        Word r=0;
        for (int i=0; i<=k; ++i)
            r = add(r, mul(trees[p.left].cut[i], trees[p.right].cut[k-i]));
        return r;
    };
    for (int k=1; k<h; ++k)
        if (coefficient(a,k)!=coefficient(b,k)) return false;
    return true;
}

std::string code(int id) {
    std::string s="(";
    for (int child: trees[id].children) s+=code(child);
    return s+")";
}

int main(int argc, char** argv) {
    int max_h = argc>1? std::atoi(argv[1]):11;
    int buckets = argc>2? std::atoi(argv[2]):1;
    int min_h = argc>3? std::atoi(argv[3]):1;
    if (max_h<min_h || min_h<1 || buckets<1) return 2;
    weight.resize(max_h+1);
    Word seed=94581231;
    for (int i=1; i<=max_h; ++i) {
        seed=add(mul(seed,seed), 98928923);
        weight[i]=seed;
    }
    for (int h=1; h<=max_h; ++h) {
        int begin=trees.size();
        std::vector<int> children;
        generate(h,h-1,0,children);
        int end=trees.size();
        if (h<min_h) continue;
        Word count=end-begin, pairs=count*(count+1)/2;
        Word seen=0, candidates=0, joint=0;
        for (int bucket=0; bucket<buckets; ++bucket) {
            std::vector<Pair> records;
            Word average = pairs / buckets;
            records.reserve(average + average/100 + 1000);
            for (int i=begin; i<end; ++i) for (int j=i; j<end; ++j) {
                Word census=add(add(trees[i].adjusted,trees[j].adjusted),
                                mul(trees[i].rooted,trees[j].rooted));
                if (census%Word(buckets)==Word(bucket)) records.push_back({census,i,j});
            }
            seen+=records.size();
            std::sort(records.begin(),records.end(),[](const Pair& a,const Pair& b){return a.census<b.census;});
            for (size_t i=0; i<records.size(); ++i) {
                for (size_t j=i+1; j<records.size() && records[i].census==records[j].census; ++j) {
                    ++candidates;
                    if (argc>4) {
                        std::cout << "candidate " << h << ' ' << code(records[i].left) << ' ' << code(records[i].right)
                                  << " | " << code(records[j].left) << ' ' << code(records[j].right) << '\n';
                    }
                    if (!same_slice(records[i],records[j],h)) continue;
                    ++joint;
                    std::cout << "survivor " << h << ' ' << code(records[i].left) << ' ' << code(records[i].right)
                              << " | " << code(records[j].left) << ' ' << code(records[j].right) << '\n';
                }
            }
        }
        if (seen!=pairs) return 3;
        std::cout<<"h="<<h<<" rooted="<<count<<" pairs="<<pairs<<" census_candidates="<<candidates
                 <<" joint_candidates="<<joint<<std::endl;
    }
}
