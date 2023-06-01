#include <bits/stdc++.h>
#include "3-uniform-hypergraph_12what.cpp"
using namespace std;

int main()
{
    auto curans = find_mu();
    auto is_valid = [&]() {
        int n = curans.size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    for (int l = 0; l < n; l++) {
                        for (int m = 0; m < 4; m++) {
                            for (int o = 0; o < 4; o++) {
                                for (int p = 0; p < 4; p++) {
                                    for (int q = 0; q < 4; q++) {
                                        set<int> all;
                                        for (auto e : curans[i][m]) {
                                            all.insert(e);
                                        }
                                        for (auto e : curans[j][o]) {
                                            all.insert(e);
                                        }
                                        for (auto e : curans[k][p]) {
                                            all.insert(e);
                                        }
                                        for (auto e : curans[l][q]) {
                                            all.insert(e);
                                        }
                                        if (all.size() == 12) {
                                            if (i == j && j == k && k == l) {
                                                continue;
                                            }
                                            else {
                                                dbg(i, m, j, o, k, p, l, q, all);
                                                return false;
                                            }
                                        }               
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        return true;
    };
    if (is_valid()) {
        cout << "HOYECHE\n";
    }
    else {
        cout << "HOLO NA\n";
    }
    cout << curans.size() << '\n';
    for (auto e : curans) {
        for (auto f : e) {
            cout << "{";
            for (auto g : f) {
                cout << g << ", ";
            }
            cout << "}, ";
        }
        cout << '\n';
    }
    cout << '\n' << '\n';
    return 0;
}
