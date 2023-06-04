#include <bits/stdc++.h>
#include "C:\Users\DARPAN\Documents\CP\debugger.h"
#define F0R(i,n) for(int i = 0; i < (n); i++)
#define FOR(i,a,b) for(int i = (a); i <= (b); i++)
#define TRAV(e,a) for(auto (e):(a))
using namespace std;

const int N = 12;

vector<vector<vector<int>>> find_mu(){
    vector<vector<vector<int>>> matchings;
    set<pair<vector<int>, vector<int>>> forbidden;
    set<vector<int>> added;
    vector<vector<int>> tuples;
    FOR(i,1,N) FOR(j,i+1,N) FOR(k,j+1,N) tuples.push_back({i,j,k});
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    shuffle(tuples.begin(),tuples.end(),rng);
    int n_tuples = tuples.size();
    F0R(i,n_tuples){
        vector<vector<int>> cur_matching;
        FOR(j,i,n_tuples-1){
            if(cur_matching.size() == 4) break;
            bool is_ok = true;
            if(added.count(tuples[j])) continue;
            TRAV(e,cur_matching){
                TRAV(f,e) TRAV(g,tuples[j]){
                    if(f == g){
                        is_ok = false;
                        break;
                    }
                }
            }
            if(!is_ok) continue;
            TRAV(e,added){
                if(forbidden.count(make_pair(e,tuples[j])) || forbidden.count(make_pair(tuples[j],e))){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            TRAV(e,added) TRAV(f,added) TRAV(g,added){
                set<int> all;
                TRAV(h,e) all.insert(h);
                TRAV(h,f) all.insert(h);
                TRAV(h,g) all.insert(h);
                TRAV(h,tuples[j]) all.insert(h);
                if(all.size() == 12){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            TRAV(e,added) TRAV(f,added) TRAV(g,cur_matching){
                set<int> all;
                TRAV(h,e) all.insert(h);
                TRAV(h,f) all.insert(h);
                TRAV(h,g) all.insert(h);
                TRAV(h,tuples[j]) all.insert(h);
                if(all.size() == 12){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            TRAV(e,added) TRAV(f,cur_matching) TRAV(g,cur_matching){
                set<int> all;
                TRAV(h,e) all.insert(h);
                TRAV(h,f) all.insert(h);
                TRAV(h,g) all.insert(h);
                TRAV(h,tuples[j]) all.insert(h);
                if(all.size() == 12){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            cur_matching.push_back(tuples[j]);
        }
        if(cur_matching.size() != 4) continue;
        sort(cur_matching.begin(),cur_matching.end());
        matchings.push_back(cur_matching);
        TRAV(e,cur_matching) added.insert(e);
        F0R(j,4){
            FOR(k,j+1,3){
                set<int> all;
                FOR(l,1,N) all.insert(l);
                TRAV(e,cur_matching[j]) all.erase(e);
                TRAV(e,cur_matching[k]) all.erase(e);
                assert(all.size() == 6);
                vector<int> rest;
                TRAV(e,all) rest.push_back(e);
                do{
                    vector<int> v1,v2;
                    F0R(l,3) v1.push_back(rest[l]);
                    FOR(l,3,5) v2.push_back(rest[l]);
                    forbidden.insert(make_pair(v1,v2));
                } while(next_permutation(rest.begin(),rest.end()));
            }
        }
    }
    sort(matchings.begin(),matchings.end());
    return matchings;
}

// int main(){
//     F0R(i,1){
//         auto answer = find_mu();
//         if(true){//answer.size() < 16 || answer.size() > 18) {
//             cout << answer.size() << '\n';
//             for (auto e : answer) {
//                 for (auto f : e) {
//                     cout << "{ ";
//                     for (auto g : f) {
//                         cout << g << ", ";
//                     }
//                     cout << "}, ";
//                 }
//                 cout << "\n";
//             }
//         }
//     }
//     return 0;
// }
