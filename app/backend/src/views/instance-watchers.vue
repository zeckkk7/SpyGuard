<template>
    <div class="backend-content" id="content">
        <div class="column col-8 col-xs-12">
            <h3 class="s-title">Gérer les instances Watchers</h3>
            <ul class="tab tab-block">
                <li class="tab-item">
                    <a href="#" v-on:click="switch_tab('addwatcher')" v-bind:class="{ active: tabs.addwatcher }">Ajouter un watcher</a>
                </li>
                <li class="tab-item">
                    <a href="#" v-on:click="switch_tab('instances')" v-bind:class="{ active: tabs.instances }">watchers déjà existants</a>
                </li>
            </ul>
            <div v-if="tabs.addwatcher">
                <div class="misp-form">
                    <label class="misp-label">nom du Watcher</label><span></span>
                    <input class="form-input" type="text" ref="watcher_name" placeholder="My incredible watcher" v-model="watcher.name" required>
                    <label class="misp-label">URL du Watcher</label><span></span>
                    <input class="form-input" type="text" ref="watcher_url" placeholder="https://url.of.my.watcher.com/watcher.json" v-model="watcher.url" required>
                    <label class="misp-label">type du Watcher</label><span></span>
                    <select class="form-select width-full" placeholder="test" v-model="watcher.type">
                        <option value="iocs">IOCs</option>
                        <option value="whitelist">Whitelist</option>
                    </select>
                </div>
                <button class="btn-primary btn col-12" v-on:click="add_instance()">Ajouter un watcher</button>
                <div class="form-group" v-if="added">
                    <div class="toast toast-success">
                        ✓ Watcher ajouté avec succès. Redirection vers le watchers dans 2 secondes. 
                    </div>
                </div>
                <div class="form-group" v-if="error">
                    <div class="toast toast-error">
                        ✗ Watcher pas ajouté. {{error}}
                    </div>
                </div>
            </div>
            <div class="form-group" v-if="tabs.instances">
                <div v-if="instances.length">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Nom</th>
                                <th>Statut</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="i in instances" v-bind:key="i.id">
                                <td>{{ i.type.toUpperCase() }}</td>
                                <td>{{ i.name }}</td>
                                <td>
                                    <span v-if="i.status" class="instance-online">✓ EN LIGNE</span>
                                    <span v-else class="instance-offline">⚠ HORS LIGNE</span>
                                </td>
                                <td><button class="btn btn-sm" v-on:click="delete_instance(i)">Supprimer</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else>
                    <div class="empty">
                        <div v-if="loading">
                            <p class="empty-title h5">
                                <span class="loading loading-lg"></span>
                            </p>
                            <p class="empty-subtitle">Test et chargment du watchers.</p>
                        </div>
                        <div v-else>
                            <p class="empty-title h5">Aucun watcher trouvé.</p>
                            <p class="empty-subtitle">N'hésitez pas à ajouter un watcher.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

import axios from 'axios'

export default {
    name: 'managewatchers',   
    data() {
        return { 
            error:false,
            loading:false,
            added:false,
            watcher:{ name:'', url:'', type:"iocs"  },
            instances:[],
            tabs: { "addwatcher" : true, "instances" : false },
            jwt:""
        }
    },
    props: { },
    methods: {
        add_instance: function()
        {  
            this.added = false;
            this.error = false;
            if (this.watcher.name && this.watcher.url && this.watcher.type)
            {
                axios.post(`/api/watchers/add`, { data: { instance: this.watcher } }, { headers: {'X-Token': this.jwt} }).then(response => {
                    if(response.data.status){
                        this.added = true;
                        setTimeout(function (){ 
                            this.switch_tab('instances')
                            this.watcher = { name:'', url:'' } 
                            this.added = false
                        }.bind(this), 2000);
                    } else {
                        this.error = response.data.message;
                    }
                })
                .catch(err => (console.log(err)))
            }
        },
        delete_instance(elem)
        {
            axios.get(`/api/watchers/delete/${elem.id}`, { timeout: 10000, headers: {'X-Token': this.jwt} })
            .then(response => {
                if(response.data.status){
                    this.instances = this.instances.filter(function(el) { return el != elem; }); 
                }
            })
            .catch(err => (console.log(err)))
        },
        get_watchers_instances()
        {
            this.loading = true;
            this.instances = []
            axios.get(`/api/watchers/get_all`, { timeout: 10000, headers: {'X-Token': this.jwt} })
            .then(response => {
                if(response.data.results){
                    this.instances = response.data.results;
                }
                this.loading = false
            })
            .catch(err => (console.log(err)))
        },
        switch_tab: function(tab) {
            Object.keys(this.tabs).forEach(key => {
                if( key == tab ){
                    this.tabs[key] = true
                    if (key == "instances") this.get_watchers_instances();
                } else {
                    this.tabs[key] = false
                }
            });
        },
        get_jwt(){
            axios.get(`/api/get-token`, { timeout: 10000 })
                .then(response => {
                    if(response.data.token){
                        this.jwt = response.data.token
                    }
                })
            .catch(err => (console.log(err)))
        }
    },
    created: function() {
        this.get_jwt();
    }
}
</script>
