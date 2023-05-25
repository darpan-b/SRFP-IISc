#include <bits/stdc++.h>
#include "C:\Users\DARPAN\Documents\CP\debugger.h"
using namespace std;


const int N = 9;

vector<vector<vector<int>>> solve() {
    // Construct the maximum number of monochormatic colourings on a hypergraph of size N
    // Till now the highest is 13, see if you can top it.

    // Brute force idea:
    // Select an arbitrary tuple (u, v, w).
    // Now for that arbitrary tuple, check how many edges cannot form edges anymore, in other words
    // strike out the invalid edges.
    // Randomly shuffle and see how that goes.

    
    /* Generate all NC3 possible tuples first */
    vector<vector<int>> tuples;
    for (int i = 1; i <= N; i++) {
        for (int j = i + 1; j <= N; j++) {
            for (int k = j + 1; k <= N; k++) {
                tuples.push_back(vector<int>{i, j, k});
            }
        }
    }

    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    shuffle(tuples.begin(), tuples.end(), rng);

    vector<vector<vector<int>>> taken;
    set<vector<int>> invalid;
    for (int i = 0; i < (int)tuples.size(); i++) {
        vector<vector<int>> cur_tuple;
        if (invalid.find(tuples[i]) != invalid.end()) continue;
        cur_tuple.push_back(tuples[i]);
        for (int j = 0; j < (int)tuples.size(); j++) {
            if (j == i) continue;
            if (invalid.find(tuples[j]) != invalid.end()) continue;
            cur_tuple.push_back(tuples[j]);
            set<int> left;
            for (int k = 1; k <= N; k++) left.insert(k);
            for (auto e : cur_tuple) for (auto f : e) left.erase(f);
            if (left.size() != 3) {
                cur_tuple = {tuples[i]};
                continue;
            }
            vector<int> last_tuple;
            for (auto e : left) last_tuple.push_back(e);
            if (invalid.find(last_tuple) != invalid.end()) {
                cur_tuple.pop_back();
                continue;
            }
            cur_tuple.push_back(last_tuple);


            // if even 1 edge is common, then it is invalid

            auto is_valid = [&]() {
                for (auto e : taken) {
                    for (auto f : e) {
                        for (auto g : cur_tuple) {
                            if (f[0] == g[0] && f[1] == g[1] && f[2] == g[2]) {
                                return false;
                            }
                        }
                    }
                }
                for (auto e : cur_tuple) {
                    if (invalid.find(e) != invalid.end()) {
                        return false;
                    }
                }
                // for (auto e : taken) {
                //     for (auto f : e) {
                //         if (invalid.find(f) != invalid.end()) {
                //             return false;
                //         }
                //     }
                // }
                return true;
            };

            if (is_valid()) {
                for (auto e : taken) {
                    for (auto f : e) {
                        set<int> left2;
                        for (auto g : cur_tuple) {
                            for (int i = 1; i <= N; i++) left2.insert(i);
                            for (auto h : g) left2.erase(h);
                            for (auto h : f) left2.erase(h);
                            vector<int> ltuple;
                            for (auto h : left2) ltuple.push_back(h);
                            if (ltuple.size() == 3) invalid.insert(ltuple);
                        }
                    }
                }
                sort(cur_tuple.begin(), cur_tuple.end());
                taken.push_back(cur_tuple);
                break;
            } else {
                cur_tuple = {tuples[i]};
            }
        }
    }

    // dbg(invalid);

    sort(taken.begin(), taken.end());
    for (auto e : taken) for (auto f : e) {
        if (invalid.find(f) != invalid.end()) {
            // dbg("F", f);
            assert(false);
        } 
    }

    return taken;
}


// 9 -> 13

int main() {
    
    for (int i = 0; i < 100000; i++) {
        auto taken = solve();
        if (taken.size() > 13) {
            cout << "TOTAL MATCHINGS = " << taken.size() << '\n';
            for (auto e : taken) {
                for (auto f : e) {
                    cout << '{' << f[0] << ", " << f[1] << ", " << f[2] << "}, "; 
                }
                cout << '\n';
            }
            cout << '\n';
        }
    }
    return 0;
}
