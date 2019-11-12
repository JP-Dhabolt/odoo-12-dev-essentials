# odoo-packt-book
Packt Book Follow-Along

## Usage
Clone the repo and move the [Odoo Addons](./odoo/addons) directory to the Odoo installation addons directory

## Development
All development work is done via Docker Compose, as it can be painful to install Odoo from source.  Any local work done
in the repo is mirrored in the repo on the Docker container (and vice versa).

### Pre-requisites
* docker-compose
* make

### Development Commands
`make` is used to coordinate the `docker-compose` commands:
* Install the addon: `make install`
* Run Odoo (exposed on `localhost:8069`): `make run`
* Test addon (also update addon): `make test`
* Remove current Odoo state (back to fresh image): `make destroy`
* Run the linter: `make lint`
* Enter interactive shell (to install new dependencies or other reasons): `make shell`
* Refresh container (will sync Pipfile.lock): `make rebuild`
* Package library: `make package`
* Start up Odoo with a REPL terminal: `make repl`
* Start up Odoo for debugging: `make debug`

### Debugging
* On the line where you want to set a breakpoint, add `import ipdb; ipdb.set_trace()`
* Startup Odoo with `make debug`
* When you hit the breakpoint, the terminal window will accept `pdb` compatible input.
* Press `h` then `Enter` for Help
* Press `c` then `Enter` to continue regulard execution.
* See [PDB Debugger Commands](https://docs.python.org/3.7/library/pdb.html#debugger-commands) for more info.
