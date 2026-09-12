import hashPassword from "../utils/password_hasher";
import pool from "../db/connect";


class User{
    constructor(id,username,password,role,is_active){
        this.id = id;
        this.username = username;
        this.password = password; 
        this.role = role;
        this.is_active = is_active;
    };

    getUserId(){
        const client = pool.connect();
        //TODO
    }
}