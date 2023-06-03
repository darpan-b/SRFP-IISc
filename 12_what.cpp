#include <bits/stdc++.h>
#include "C:\Users\DARPAN\Documents\CP\debugger.h"
#define F0R(i,n) for(int i = 0; i < (n); i++)
#define FOR(i,a,b) for(int i = (a); i <= (b); i++)
using namespace std;

const int N = 12;

vector<vector<vector<int>>> find_mu(){
    vector<vector<int>> tuples;
    FOR(i,1,N) FOR(j,i+1,N) FOR(k,j+1,N) tuples.push_back({i,j,k});
    int n_tuples = tuples.size();
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    shuffle(tuples.begin(),tuples.end(),rng);
    vector<vector<vector<int>>> matchings;
    set<pair<vector<int>, vector<int>>> forbidden;
    set<vector<int>> added;
    F0R(i,n_tuples){
        bool can_be_added = true;
        for(auto e:added){
            if(forbidden.count(make_pair(e,tuples[i])) || forbidden.count(make_pair(tuples[i],e))){
                can_be_added = false;
                break;
            }
        }
        if(!can_be_added || added.count(tuples[i])) continue;
        vector<vector<int>> cur_matching = {tuples[i]};
        FOR(j,i+1,n_tuples-1){
            if(cur_matching.size() == 4) break;
            if(added.count(tuples[j])) continue;
            bool is_ok = true;
            for(auto e:added){
                if(forbidden.count(make_pair(e,tuples[j])) || forbidden.count(make_pair(tuples[j],e))){
                    is_ok = false;
                    break;
                }
            }
            for(auto e:cur_matching){
                if(forbidden.count(make_pair(e,tuples[j])) || forbidden.count(make_pair(tuples[j],e))){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            for(auto e:added) for(auto f:added) for(auto g:added){
                set<int> allnums;
                for(auto h:e) allnums.insert(h);
                for(auto h:f) allnums.insert(h);
                for(auto h:g) allnums.insert(h);
                for(auto h:tuples[j]) allnums.insert(h);
                if(allnums.size() == 12){
                    is_ok = false;
                    break;
                }
            }
            if(!is_ok) continue;
            cur_matching.push_back(tuples[j]);
        }
        if(cur_matching.size() != 4) continue;
        matchings.push_back(cur_matching);
        for(auto e:cur_matching) added.insert(e);
        F0R(j,4){
            FOR(k,j+1,3){
                set<int> all_here;
                FOR(l,1,12) all_here.insert(l);
                for(auto e:cur_matching[j]) all_here.erase(e);
                for(auto e:cur_matching[k]) all_here.erase(e);
                vector<int> rest;
                for(auto e:all_here) rest.push_back(e);
                do{
                    vector<int> v1,v2;
                    F0R(l,3) v1.push_back(rest[l]);
                    FOR(l,3,5) v2.push_back(rest[l]);
                    forbidden.insert(make_pair(v1,v2));
                } while(next_permutation(rest.begin(),rest.end()));
            }
        }
    }
    return matchings;
}

// int main(){
//     auto answer = find_mu();
//     cout << answer.size() << '\n';
//     for (auto e : answer) {
//         for (auto f : e) {
//             cout << "{ ";
//             for (auto g : f) {
//                 cout << g << ", ";
//             }
//             cout << "}, ";
//         }
//         cout << "\n";
//     }
//     return 0;
// }
