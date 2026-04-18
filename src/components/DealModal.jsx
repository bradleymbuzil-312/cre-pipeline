import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { X, ChevronDown, ChevronUp, Plus, Trash2, CheckSquare, Square, MapPin, ExternalLink } from 'lucide-react'
import { STAGES, PROPERTY_TYPES } from '../lib/constants'
import ActivityLog, { logActivity } from './ActivityLog'
import DealLinks from './DealLinks'
import { useToast } from './Toast'

const FINANCE_PURPOSES = ['Acquisition','Refinance','Construction','Bridge','Mezzanine','Preferred Equity','Recapitalization','Other']
const CAPITAL_TYPES = ['Debt','Equity','Preferred Equity','Mezzanine']
const DEBT_EQUITY_TYPES = ['Permanent','Bridge','Construction','Mini-Perm','CMBS','Agency','SBA','Life Company','Bank','Credit Union','Debt Fund','Other']
const FEE_TYPES = ['Percentage','Flat Fee']
const RATE_TYPES = ['Fixed','Floating','Fixed to Floating']
const RATE_INDEXES = ['SOFR','Prime','Treasury','LIBOR','Other']
const RECOURSE_TYPES = ['Full Recourse','Non-Recourse','Partial Recourse','Carve-Out Guaranty']
const FEE_AGREEMENT_TYPES = ['Exclusive','Non-Exclusive','Right of First Refusal']
const PRIORITIES = ['High','Medium','Low']

const EMPTY = {
  borrower_name:'',stage:'Engagement',expected_close_date:'',
  property_id:'',referral_source_id:'',
  property_address:'',city:'',state_province:'',zip_code:'',
  property_type:'',total_units:'',sq_ft:'',year_built:'',
  loan_amount:'',finance_purpose:'',capital_type:'Debt',debt_equity_type:'',
  lender_name:'',term_months:'',amortization_months:'',io_months:'',
  interest_rate_type:'',interest_rate_index:'',base_rate:'',spread_bps:'',
  interest_rate:'',ltv:'',dscr:'',recourse:'',
  maturity_date:'',prepay_penalty_exp:'',prepay_description:'',capital_notes:'',
  capital_exit_fee_pct:'',capital_exit_fee_amt:'',
  origination_fee_type:'Percentage',origination_fee_pct:'',
  origination_fee_amt:'',commission_fee:'',
  fee_agreement_type:'Exclusive',engagement_date:'',
  term_sheet_date:'',rate_lock_date:'',x1031_exchange:false,
  referral_source:'',referred_by:'',referral_notes:'',notes:'',
}

const IS = {width:'100%',background:'var(--surface2)',border:'1px solid var(--border)',color:'var(--text)',borderRadius:'6px',padding:'7px 10px',fontSize:'12px',fontFamily:'DM Sans, sans-serif',boxSizing:'border-box'}
const LS = {display:'block',marginBottom:'4px',fontSize:'10px',fontWeight:700,color:'var(--muted)',fontFamily:'Syne, sans-serif',textTransform:'uppercase',letterSpacing:'0.08em'}

function F({label,children,span}){return <div style={{gridColumn:span===2?'span 2':span===3?'1 / -1':'auto'}}><label style={LS}>{label}</label>{children}</div>}
function Sel({value,onChange,options}){return <select value={value} onChange={onChange} style={IS}><option value="">Select...</option>{options.map(o=><option key={o} value={o}>{o}</option>)}</select>}
function Inp({type='text',value,onChange,placeholder,step}){return <input type={type} value={value} onChange={onChange} placeholder={placeholder} step={step} style={IS}/>}

function Section({title,children,defaultOpen=true,badge}){
  const [open,setOpen]=useState(defaultOpen)
  return(
    <div style={{marginBottom:'4px'}}>
      <button type="button" onClick={()=>setOpen(o=>!o)} style={{width:'100%',display:'flex',alignItems:'center',justifyContent:'space-between',background:'var(--surface2)',border:'1px solid var(--border)',color:'var(--text)',padding:'7px 12px',borderRadius:'6px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'11px',letterSpacing:'0.06em',textTransform:'uppercase',marginBottom:open?'12px':'0'}}>
        <div style={{display:'flex',alignItems:'center',gap:'8px'}}>
          {title}
          {badge > 0 && <span style={{background:'#2563eb',color:'#fff',borderRadius:'9px',padding:'1px 6px',fontSize:'9px',fontWeight:700}}>{badge}</span>}
        </div>
        {open?<ChevronUp size={13}/>:<ChevronDown size={13}/>}
      </button>
      {open && <div style={{paddingBottom:'14px'}}>{children}</div>}
    </div>
  )
}

function DealTasks({dealId, session, teamMembers}){
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [newTask, setNewTask] = useState({title:'',assigned_to:'',priority:'Medium',due_date:'',description:''})

  useEffect(()=>{ if(dealId) fetchTasks() }, [dealId])

  async function fetchTasks(){
    const {data} = await supabase.from('tasks').select('*').eq('deal_id', dealId).order('created_at')
    setTasks(data||[])
    setLoading(false)
  }

  async function addTask(){
    if(!newTask.title.trim()) return
    const {error} = await supabase.from('tasks').insert({
      title: newTask.title.trim(),
      description: newTask.description.trim()||null,
      assigned_to: newTask.assigned_to||null,
      priority: newTask.priority,
      due_date: newTask.due_date||null,
      status: 'To Do',
      deal_id: dealId,
      created_by: session.user.id
    })
    if(!error){
      setNewTask({title:'',assigned_to:'',priority:'Medium',due_date:'',description:''})
      setAdding(false)
      fetchTasks()
    }
  }

  async function toggleStatus(task){
    const status = task.status === 'Done' ? 'To Do' : 'Done'
    await supabase.from('tasks').update({status, updated_at: new Date().toISOString()}).eq('id', task.id)
    fetchTasks()
  }

  async function deleteTask(id){
    if(!window.confirm('Delete this task?')) return
    await supabase.from('tasks').delete().eq('id', id)
    fetchTasks()
  }

  const PRIORITY_COLORS = {High:'#ef4444',Medium:'#c2410c',Low:'#2563eb'}

  return(
    <div style={{display:'flex',flexDirection:'column',gap:'8px'}}>
      {loading ? (
        <div style={{fontSize:'11px',color:'var(--muted)',fontFamily:'IBM Plex Mono, monospace'}}>LOADING TASKS...</div>
      ) : tasks.length === 0 && !adding ? (
        <div style={{fontSize:'12px',color:'var(--muted)',padding:'12px',background:'var(--surface2)',borderRadius:'6px',textAlign:'center'}}>No tasks yet for this deal</div>
      ) : (
        tasks.map(task => (
          <div key={task.id} style={{display:'flex',alignItems:'flex-start',gap:'8px',padding:'8px 10px',background:'var(--surface2)',borderRadius:'6px',border:'1px solid var(--border)'}}>
            <button onClick={()=>toggleStatus(task)} style={{background:'transparent',border:'none',cursor:'pointer',color:task.status==='Done'?'#16a34a':'var(--muted)',padding:'1px',flexShrink:0,marginTop:'1px'}}>
              {task.status==='Done'?<CheckSquare size={14}/>:<Square size={14}/>}
            </button>
            <div style={{flex:1,minWidth:0}}>
              <div style={{fontSize:'12px',fontWeight:600,color:task.status==='Done'?'var(--muted)':'var(--text)',textDecoration:task.status==='Done'?'line-through':'none',fontFamily:'Syne, sans-serif',marginBottom:'2px'}}>{task.title}</div>
              <div style={{display:'flex',gap:'8px',alignItems:'center',flexWrap:'wrap'}}>
                <span style={{fontSize:'9px',padding:'1px 5px',borderRadius:'3px',background:'var(--surface)',color:PRIORITY_COLORS[task.priority]||'var(--muted)',border:'1px solid '+(PRIORITY_COLORS[task.priority]||'var(--border)')+'33',fontFamily:'Syne, sans-serif',fontWeight:700,textTransform:'uppercase'}}>{task.priority}</span>
                {task.assigned_to && <span style={{fontSize:'10px',color:'var(--muted)'}}>{task.assigned_to}</span>}
                {task.due_date && <span style={{fontSize:'10px',color:'var(--muted)',fontFamily:'IBM Plex Mono, monospace'}}>{new Date(task.due_date+'T00:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric'})}</span>}
              </div>
              {task.description && <div style={{fontSize:'11px',color:'var(--muted)',marginTop:'3px',lineHeight:1.4}}>{task.description}</div>}
            </div>
            <button onClick={()=>deleteTask(task.id)} style={{background:'transparent',border:'none',cursor:'pointer',color:'var(--muted)',padding:'2px',flexShrink:0}} onMouseEnter={e=>e.currentTarget.style.color='#ef4444'} onMouseLeave={e=>e.currentTarget.style.color='var(--muted)'}><Trash2 size={11}/></button>
          </div>
        ))
      )}

      {adding && (
        <div style={{background:'var(--surface2)',border:'1px solid #2563eb',borderRadius:'6px',padding:'12px',display:'flex',flexDirection:'column',gap:'8px'}}>
          <input value={newTask.title} onChange={e=>setNewTask(t=>({...t,title:e.target.value}))} placeholder="Task title *" autoFocus style={{...IS,fontSize:'13px'}} onKeyDown={e=>e.key==='Enter'&&addTask()}/>
          <textarea value={newTask.description} onChange={e=>setNewTask(t=>({...t,description:e.target.value}))} placeholder="Description (optional)" rows={2} style={{...IS,resize:'none',lineHeight:1.5}}/>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'8px'}}>
            <div>
              <label style={LS}>Assign To</label>
              <select value={newTask.assigned_to} onChange={e=>setNewTask(t=>({...t,assigned_to:e.target.value}))} style={IS}>
                <option value="">Unassigned</option>
                {(teamMembers||[]).map(m=><option key={m.id} value={m.name}>{m.name}</option>)}
              </select>
            </div>
            <div>
              <label style={LS}>Priority</label>
              <select value={newTask.priority} onChange={e=>setNewTask(t=>({...t,priority:e.target.value}))} style={IS}>
                {PRIORITIES.map(p=><option key={p} value={p}>{p}</option>)}
              </select>
            </div>
            <div>
              <label style={LS}>Due Date</label>
              <input type="date" value={newTask.due_date} onChange={e=>setNewTask(t=>({...t,due_date:e.target.value}))} style={IS}/>
            </div>
          </div>
          <div style={{display:'flex',gap:'6px',justifyContent:'flex-end'}}>
            <button onClick={()=>{setAdding(false);setNewTask({title:'',assigned_to:'',priority:'Medium',due_date:'',description:''})}} style={{background:'transparent',border:'1px solid var(--border)',color:'var(--muted)',padding:'6px 12px',borderRadius:'5px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:600,fontSize:'11px'}}>CANCEL</button>
            <button onClick={addTask} style={{background:'#2563eb',border:'none',color:'#fff',padding:'6px 16px',borderRadius:'5px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'11px'}}>ADD TASK</button>
          </div>
        </div>
      )}

      {!adding && (
        <button onClick={()=>setAdding(true)} style={{display:'flex',alignItems:'center',gap:'5px',background:'transparent',border:'1px dashed var(--border)',borderRadius:'6px',color:'var(--muted)',padding:'8px 12px',cursor:'pointer',fontSize:'11px',fontFamily:'Syne, sans-serif',fontWeight:600,width:'100%',justifyContent:'center'}} onMouseEnter={e=>{e.currentTarget.style.borderColor='#2563eb';e.currentTarget.style.color='#2563eb'}} onMouseLeave={e=>{e.currentTarget.style.borderColor='var(--border)';e.currentTarget.style.color='var(--muted)'}}>
          <Plus size={11}/> ADD TASK TO THIS DEAL
        </button>
      )}
    </div>
  )
}

export default function DealModal({deal, session, onClose, onSaved}){
  const [form,setForm]=useState(()=>{
    if(!deal)return{...EMPTY}
    const f={...EMPTY,...deal}
    Object.keys(f).forEach(k=>{if(f[k]===null||f[k]===undefined)f[k]=''})
    f.x1031_exchange=!!deal.x1031_exchange
    return f
  })
  const [saving,setSaving]=useState(false)
  const [error,setError]=useState('')
  const [teamMembers,setTeamMembers]=useState([])
  const [properties,setProperties]=useState([])
  const [referralSources,setReferralSources]=useState([])
  const { toast } = useToast()

  useEffect(()=>{
    supabase.from('team_members').select('*').order('name').then(({data})=>setTeamMembers(data||[]))
    supabase.from('properties').select('id, address, city, state').order('address').then(({data})=>setProperties(data||[]))
    supabase.from('clients').select('id, first_name, last_name, company').eq('client_type', 'Referral Source').order('first_name').then(({data})=>setReferralSources(data||[]))
  },[])

  function set(k,v){setForm(f=>({...f,[k]:v}))}
  function num(v){return v!==''?parseFloat(v):null}
  function int(v){return v!==''?parseInt(v):null}
  function str(v){return v?.trim()||null}
  function dt(v){return v||null}

  function fullAddress(){
    return [form.property_address, form.city, form.state_province, form.zip_code].filter(Boolean).join(', ')
  }

  function openReonomy(){
    const q = fullAddress()
    if(!q){ toast('Add a property address first', 'info'); return }
    window.open('https://app.reonomy.com/!/search?q=' + encodeURIComponent(q), '_blank', 'noopener')
  }

  function openMaps(){
    const q = fullAddress()
    if(!q){ toast('Add a property address first', 'info'); return }
    window.open('https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(q), '_blank', 'noopener')
  }

  async function handleSave(){
    if(!form.borrower_name.trim()){setError('Borrower name is required.');return}
    setSaving(true);setError('')
    const p={
      borrower_name:str(form.borrower_name),stage:form.stage,expected_close_date:dt(form.expected_close_date),
      property_id: form.property_id || null,
      referral_source_id: form.referral_source_id || null,
      property_address:str(form.property_address),city:str(form.city),state_province:str(form.state_province),zip_code:str(form.zip_code),
      property_type:str(form.property_type),total_units:int(form.total_units),sq_ft:num(form.sq_ft),year_built:int(form.year_built),
      loan_amount:num(form.loan_amount),finance_purpose:str(form.finance_purpose),capital_type:str(form.capital_type),debt_equity_type:str(form.debt_equity_type),
      lender_name:str(form.lender_name),term_months:int(form.term_months),amortization_months:int(form.amortization_months),io_months:int(form.io_months),
      interest_rate_type:str(form.interest_rate_type),interest_rate_index:str(form.interest_rate_index),
      base_rate:num(form.base_rate),spread_bps:int(form.spread_bps),interest_rate:num(form.interest_rate),
      ltv:num(form.ltv),dscr:num(form.dscr),recourse:str(form.recourse),
      maturity_date:dt(form.maturity_date),prepay_penalty_exp:dt(form.prepay_penalty_exp),
      prepay_description:str(form.prepay_description),capital_notes:str(form.capital_notes),
      capital_exit_fee_pct:num(form.capital_exit_fee_pct),capital_exit_fee_amt:num(form.capital_exit_fee_amt),
      origination_fee_type:str(form.origination_fee_type),origination_fee_pct:num(form.origination_fee_pct),
      origination_fee_amt:num(form.origination_fee_amt),commission_fee:num(form.commission_fee),
      fee_agreement_type:str(form.fee_agreement_type),engagement_date:dt(form.engagement_date),
      term_sheet_date:dt(form.term_sheet_date),rate_lock_date:dt(form.rate_lock_date),x1031_exchange:!!form.x1031_exchange,
      referral_source:str(form.referral_source),referred_by:str(form.referred_by),referral_notes:str(form.referral_notes),
      notes:str(form.notes),updated_at:new Date().toISOString(),
    }
    let err, savedId = deal?.id
    const oldStage = deal?.stage
    if(deal?.id){
      ;({error:err} = await supabase.from('deals').update(p).eq('id',deal.id))
    } else {
      const { data: inserted, error: insertErr } = await supabase.from('deals').insert({...p,created_by:session.user.id}).select().single()
      err = insertErr
      savedId = inserted?.id
    }
    if(err){setError(err.message);setSaving(false);return}

    if (savedId) {
      if (!deal?.id) {
        await logActivity(savedId, session.user.id, session.user.email, 'deal_created', 'Created deal for ' + p.borrower_name)
      } else if (oldStage !== p.stage) {
        await logActivity(savedId, session.user.id, session.user.email, 'stage_changed', 'Stage changed from ' + oldStage + ' to ' + p.stage, oldStage, p.stage)
      } else {
        await logActivity(savedId, session.user.id, session.user.email, 'deal_updated', 'Updated deal details')
      }
    }

    toast(deal?.id ? 'Deal saved' : 'Deal created', 'success')
    onSaved();onClose()
  }

  function propertyLabel(p) {
    return p.address + (p.city ? (', ' + p.city) : '') + (p.state ? ', ' + p.state : '')
  }
  function borrowerLabel(b) {
    return (b.first_name + ' ' + (b.last_name || '')).trim() + (b.company ? ' \u2014 ' + b.company : '')
  }

  const hasPropAddress = !!form.property_address
  const extBtn = (enabled) => ({ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', color: enabled ? 'var(--text)' : 'var(--muted)', border: '1px solid var(--border)', padding: '6px 11px', borderRadius: '5px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '10.5px', cursor: enabled ? 'pointer' : 'not-allowed', letterSpacing: '0.04em', opacity: enabled ? 1 : 0.5 })

  return(
    <div onClick={e=>{if(e.target===e.currentTarget)onClose()}} style={{position:'fixed',inset:0,zIndex:1000,background:'rgba(0,0,0,0.4)',backdropFilter:'blur(4px)',display:'flex',alignItems:'center',justifyContent:'center',padding:'16px'}}>
      <div style={{background:'var(--surface)',border:'1px solid var(--border)',borderRadius:'12px',width:'100%',maxWidth:'900px',maxHeight:'94vh',display:'flex',flexDirection:'column',boxShadow:'0 24px 60px rgba(0,0,0,0.12)'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'16px 22px',borderBottom:'1px solid var(--border)',flexShrink:0}}>
          <div>
            <h2 style={{fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'16px',color:'var(--text)',marginBottom:'1px'}}>{deal?'Edit Deal':'New Deal'}</h2>
            {deal && <div style={{fontSize:'11px',color:'var(--muted)',fontFamily:'IBM Plex Mono, monospace'}}>{deal.borrower_name}</div>}
          </div>
          <button onClick={onClose} style={{background:'transparent',border:'1px solid var(--border)',color:'var(--muted)',cursor:'pointer',padding:'5px',borderRadius:'6px',display:'flex',alignItems:'center'}}><X size={15}/></button>
        </div>

        <div style={{overflowY:'auto',flex:1,padding:'16px 22px',display:'flex',flexDirection:'column',gap:'4px'}}>
          <Section title="Summary">
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px'}}>
              <F label="Borrower / Client *"><Inp value={form.borrower_name} onChange={e=>set('borrower_name',e.target.value)} placeholder="Name"/></F>
              <F label="Stage"><Sel value={form.stage} onChange={e=>set('stage',e.target.value)} options={STAGES}/></F>
              <F label="Close Date"><Inp type="date" value={form.expected_close_date} onChange={e=>set('expected_close_date',e.target.value)}/></F>
              <F label="Proceeds / Loan Amount ($)"><Inp type="number" value={form.loan_amount} onChange={e=>set('loan_amount',e.target.value)} placeholder="27500000"/></F>
              <F label="Finance Purpose"><Sel value={form.finance_purpose} onChange={e=>set('finance_purpose',e.target.value)} options={FINANCE_PURPOSES}/></F>
              <F label="Capital Type"><Sel value={form.capital_type} onChange={e=>set('capital_type',e.target.value)} options={CAPITAL_TYPES}/></F>
              <F label="Debt / Equity Type"><Sel value={form.debt_equity_type} onChange={e=>set('debt_equity_type',e.target.value)} options={DEBT_EQUITY_TYPES}/></F>
              <F label="Fee Agreement Type"><Sel value={form.fee_agreement_type} onChange={e=>set('fee_agreement_type',e.target.value)} options={FEE_AGREEMENT_TYPES}/></F>
              <F label="1031 Exchange"><div style={{display:'flex',alignItems:'center',gap:'8px',paddingTop:'6px'}}><input type="checkbox" checked={!!form.x1031_exchange} onChange={e=>set('x1031_exchange',e.target.checked)} style={{width:'14px',height:'14px',accentColor:'#2563eb',cursor:'pointer'}}/><span style={{fontSize:'12px',color:'var(--muted)'}}>Yes</span></div></F>
            </div>
          </Section>

          <Section title="Links">
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'10px 14px'}}>
              <F label="Link to Property">
                <select value={form.property_id} onChange={e=>set('property_id',e.target.value)} style={IS}>
                  <option value="">No property linked</option>
                  {properties.map(p=><option key={p.id} value={p.id}>{propertyLabel(p)}</option>)}
                </select>
              </F>
              <F label="Referral Source">
                <select value={form.referral_source_id} onChange={e=>set('referral_source_id',e.target.value)} style={IS}>
                  <option value="">No referral source</option>
                  {referralSources.map(r=><option key={r.id} value={r.id}>{borrowerLabel(r)}</option>)}
                </select>
              </F>
            </div>
            <div style={{fontSize:'11px',color:'var(--muted)',marginTop:'10px',lineHeight:1.5}}>Linking a property shows this deal on the property card in the Properties tab. Linking a referral source helps you track which deals came from each referrer.</div>
          </Section>

          {deal?.id && (
            <Section title="Documents (OneDrive Links)" defaultOpen={true}>
              <DealLinks dealId={deal.id} session={session} />
            </Section>
          )}

          <Section title="Property Details" defaultOpen={false}>
            <div style={{display:'flex',gap:'8px',marginBottom:'12px',flexWrap:'wrap'}}>
              <button onClick={openReonomy} disabled={!hasPropAddress} title={hasPropAddress ? 'Open Reonomy with this address pre-filled' : 'Add a property address to enable'} style={extBtn(hasPropAddress)}>
                <ExternalLink size={11}/> LOOK UP ON REONOMY
              </button>
              <button onClick={openMaps} disabled={!hasPropAddress} title={hasPropAddress ? 'Open Google Maps with this address' : 'Add a property address to enable'} style={extBtn(hasPropAddress)}>
                <MapPin size={11}/> VIEW ON MAPS
              </button>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px'}}>
              <F label="Property Type"><Sel value={form.property_type} onChange={e=>set('property_type',e.target.value)} options={PROPERTY_TYPES}/></F>
              <F label="Address" span={2}><Inp value={form.property_address} onChange={e=>set('property_address',e.target.value)} placeholder="111 San Bruno Ave W"/></F>
              <F label="City"><Inp value={form.city} onChange={e=>set('city',e.target.value)} placeholder="San Bruno"/></F>
              <F label="State / Province"><Inp value={form.state_province} onChange={e=>set('state_province',e.target.value)} placeholder="California"/></F>
              <F label="Zip / Postal Code"><Inp value={form.zip_code} onChange={e=>set('zip_code',e.target.value)} placeholder="94066"/></F>
              <F label="Total Units"><Inp type="number" value={form.total_units} onChange={e=>set('total_units',e.target.value)} placeholder="46"/></F>
              <F label="Property Size (Sq Ft)"><Inp type="number" value={form.sq_ft} onChange={e=>set('sq_ft',e.target.value)} placeholder="111400"/></F>
              <F label="Year Built"><Inp type="number" value={form.year_built} onChange={e=>set('year_built',e.target.value)} placeholder="2020"/></F>
            </div>
          </Section>

          <Section title="Capital Details" defaultOpen={false}>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px'}}>
              <F label="Capital Source (Lender)"><Inp value={form.lender_name} onChange={e=>set('lender_name',e.target.value)} placeholder="East West Bank"/></F>
              <F label="Term (Months)"><Inp type="number" value={form.term_months} onChange={e=>set('term_months',e.target.value)} placeholder="360"/></F>
              <F label="Amortization (Months)"><Inp type="number" value={form.amortization_months} onChange={e=>set('amortization_months',e.target.value)} placeholder="360"/></F>
              <F label="I/O (Months)"><Inp type="number" value={form.io_months} onChange={e=>set('io_months',e.target.value)} placeholder="24"/></F>
              <F label="Interest Rate Type"><Sel value={form.interest_rate_type} onChange={e=>set('interest_rate_type',e.target.value)} options={RATE_TYPES}/></F>
              <F label="Interest Rate Index"><Sel value={form.interest_rate_index} onChange={e=>set('interest_rate_index',e.target.value)} options={RATE_INDEXES}/></F>
              <F label="Base Rate (%)"><Inp type="number" value={form.base_rate} onChange={e=>set('base_rate',e.target.value)} placeholder="5.25" step="0.01"/></F>
              <F label="Spread (bps)"><Inp type="number" value={form.spread_bps} onChange={e=>set('spread_bps',e.target.value)} placeholder="250"/></F>
              <F label="Interest Rate (%)"><Inp type="number" value={form.interest_rate} onChange={e=>set('interest_rate',e.target.value)} placeholder="6.50" step="0.01"/></F>
              <F label="LTV/LTC (%)"><Inp type="number" value={form.ltv} onChange={e=>set('ltv',e.target.value)} placeholder="65" step="0.1"/></F>
              <F label="DSCR"><Inp type="number" value={form.dscr} onChange={e=>set('dscr',e.target.value)} placeholder="1.25" step="0.01"/></F>
              <F label="Recourse"><Sel value={form.recourse} onChange={e=>set('recourse',e.target.value)} options={RECOURSE_TYPES}/></F>
              <F label="Maturity Date"><Inp type="date" value={form.maturity_date} onChange={e=>set('maturity_date',e.target.value)}/></F>
              <F label="Prepay Penalty Exp Date"><Inp type="date" value={form.prepay_penalty_exp} onChange={e=>set('prepay_penalty_exp',e.target.value)}/></F>
              <F label="Prepay Description"><Inp value={form.prepay_description} onChange={e=>set('prepay_description',e.target.value)} placeholder="5-4-3-2-1 step-down"/></F>
              <F label="Capital Exit Fee (%)"><Inp type="number" value={form.capital_exit_fee_pct} onChange={e=>set('capital_exit_fee_pct',e.target.value)} placeholder="1.00" step="0.01"/></F>
              <F label="Capital Exit Fee ($)"><Inp type="number" value={form.capital_exit_fee_amt} onChange={e=>set('capital_exit_fee_amt',e.target.value)} placeholder="275000"/></F>
              <F label="Capital Notes" span={3}><textarea value={form.capital_notes} onChange={e=>set('capital_notes',e.target.value)} rows={2} placeholder="Lender-specific notes..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
            </div>
          </Section>

          <Section title="Fee Details" defaultOpen={false}>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px'}}>
              <F label="Origination Fee Type"><Sel value={form.origination_fee_type} onChange={e=>set('origination_fee_type',e.target.value)} options={FEE_TYPES}/></F>
              <F label="Origination Fee (%)"><Inp type="number" value={form.origination_fee_pct} onChange={e=>set('origination_fee_pct',e.target.value)} placeholder="1.000" step="0.001"/></F>
              <F label="Origination Fee ($)"><Inp type="number" value={form.origination_fee_amt} onChange={e=>set('origination_fee_amt',e.target.value)} placeholder="275000"/></F>
              <F label="Total Commission / Fee ($)"><Inp type="number" value={form.commission_fee} onChange={e=>set('commission_fee',e.target.value)} placeholder="275000"/></F>
              <F label="Engagement Executed Date"><Inp type="date" value={form.engagement_date} onChange={e=>set('engagement_date',e.target.value)}/></F>
              <F label="Term Sheet / LOI Date"><Inp type="date" value={form.term_sheet_date} onChange={e=>set('term_sheet_date',e.target.value)}/></F>
              <F label="Rate Lock Date"><Inp type="date" value={form.rate_lock_date} onChange={e=>set('rate_lock_date',e.target.value)}/></F>
            </div>
          </Section>

          <Section title="Referral Notes" defaultOpen={false}>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px'}}>
              <F label="Referral Source (free text)"><Inp value={form.referral_source} onChange={e=>set('referral_source',e.target.value)} placeholder="John Smith"/></F>
              <F label="Referred By"><Inp value={form.referred_by} onChange={e=>set('referred_by',e.target.value)} placeholder="Internal or external"/></F>
              <F label="Referral Notes" span={3}><textarea value={form.referral_notes} onChange={e=>set('referral_notes',e.target.value)} rows={2} placeholder="Referral context..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
            </div>
          </Section>

          <Section title="General Notes" defaultOpen={false}>
            <div style={{display:'grid',gridTemplateColumns:'1fr',gap:'10px'}}>
              <F label="Notes / Next Steps" span={3}><textarea value={form.notes} onChange={e=>set('notes',e.target.value)} rows={3} placeholder="Key next steps, outstanding items, lender notes..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
            </div>
          </Section>

          {deal?.id && (
            <Section title="Tasks" defaultOpen={true}>
              <DealTasks dealId={deal.id} session={session} teamMembers={teamMembers}/>
            </Section>
          )}

          {deal?.id && (
            <Section title="Activity History" defaultOpen={false}>
              <ActivityLog dealId={deal.id} />
            </Section>
          )}

          {!deal?.id && (
            <div style={{padding:'10px 14px',borderRadius:'6px',background:'var(--surface2)',border:'1px solid var(--border)',fontSize:'11px',color:'var(--muted)'}}>
              Save this deal first, then reopen it to add documents, tasks, and see activity history.
            </div>
          )}

          {error && <div style={{padding:'10px 14px',borderRadius:'6px',background:'#fef2f2',border:'1px solid #fecaca',color:'#ef4444',fontSize:'13px'}}>{error}</div>}
        </div>

        <div style={{padding:'12px 22px',borderTop:'1px solid var(--border)',display:'flex',justifyContent:'flex-end',gap:'10px',flexShrink:0}}>
          <button onClick={onClose} style={{background:'transparent',border:'1px solid var(--border)',color:'var(--text)',padding:'8px 20px',borderRadius:'6px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:600,fontSize:'12px',letterSpacing:'0.04em'}}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{background:saving?'#93c5fd':'#2563eb',border:'none',color:'#fff',padding:'8px 24px',borderRadius:'6px',cursor:saving?'not-allowed':'pointer',fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'12px',letterSpacing:'0.04em'}}>{saving?'SAVING...':deal?'SAVE CHANGES':'ADD DEAL'}</button>
        </div>
      </div>
    </div>
  )
}