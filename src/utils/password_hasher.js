import crypto from "crypto";

function hashPassword(password) {
    return new Promise((resolve, reject) => {
        const salt = crypto.randomBytes(16).toString("hex");

        crypto.scrypt(password, salt, 64, (err, derivedKey) => {
            if (err) reject(err);

            resolve(`${salt}:${derivedKey.toString("hex")}`);
        });
    });
}

export default hashPassword;